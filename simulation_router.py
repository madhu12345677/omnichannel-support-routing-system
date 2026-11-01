
import sqlite3

DB_PATH = "database/support_system.db"

PRIORITY_ORDER = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4
}

INTENT_SKILL_MAP = {
    "Order Status": "Order Management",
    "Refund": "Refund",
    "Payment Issue": "Billing",
    "Account Access": "Account Support",
    "Product Information": "Product Support",
    "Technical Support": "Technical",
    "Cancellation": "General Support",
    "Complaint": "Complaints",
}


def run_simulation():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        cursor = conn.cursor()
        cursor.execute("BEGIN IMMEDIATE")

        # Get active agents and their capacity
        cursor.execute("""
            SELECT agent_id, max_concurrent_tickets
            FROM agents
            WHERE status = 'Active'
        """)
        agents = {
            agent_id: {
                "capacity": capacity,
                "workload": 0,
                "skills": set(),
                "languages": set()
            }
            for agent_id, capacity in cursor.fetchall()
        }

        # Load existing simulation workload
        cursor.execute("""
            SELECT agent_id, COUNT(*)
            FROM simulation_assignments
            WHERE status = 'Active'
            GROUP BY agent_id
        """)
        for agent_id, count in cursor.fetchall():
            if agent_id in agents:
                agents[agent_id]["workload"] = count

        # Load agent skills
        cursor.execute("""
            SELECT agent_id, skill_id
            FROM agent_skills
        """)
        for agent_id, skill_id in cursor.fetchall():
            if agent_id in agents:
                agents[agent_id]["skills"].add(skill_id)

        # Load agent languages
        cursor.execute("""
            SELECT agent_id, language_id
            FROM agent_languages
        """)
        for agent_id, language_id in cursor.fetchall():
            if agent_id in agents:
                agents[agent_id]["languages"].add(language_id)

        # Convert skill names to IDs
        cursor.execute("SELECT skill_id, skill_name FROM skills")
        skill_ids = {
            name: skill_id
            for skill_id, name in cursor.fetchall()
        }

        # Get waiting tickets not already simulated
        cursor.execute("""
            SELECT
                oq.ticket_id,
                oq.priority,
                t.language_id,
                i.intent_name
            FROM overflow_queue oq
            JOIN tickets t ON oq.ticket_id = t.ticket_id
            JOIN intents i ON t.intent_id = i.intent_id
            WHERE oq.status = 'Waiting'
              AND NOT EXISTS (
                  SELECT 1
                  FROM simulation_assignments sa
                  WHERE sa.ticket_id = oq.ticket_id
              )
        """)

        tickets = cursor.fetchall()
        tickets.sort(
            key=lambda row: PRIORITY_ORDER.get(row[1], 5)
        )

        assigned_count = 0
        waiting_count = 0

        for ticket_id, priority, language_id, intent in tickets:

            required_skill = skill_ids.get(
                INTENT_SKILL_MAP.get(intent)
            )

            if required_skill is None:
                waiting_count += 1
                continue

            eligible_agents = []

            for agent_id, details in agents.items():

                if details["workload"] >= details["capacity"]:
                    continue

                if required_skill not in details["skills"]:
                    continue

                if language_id not in details["languages"]:
                    continue

                eligible_agents.append(agent_id)

            if not eligible_agents:
                waiting_count += 1
                continue

            # Choose the least-loaded eligible agent
            selected_agent = min(
                eligible_agents,
                key=lambda aid: (
                    agents[aid]["workload"],
                    aid
                )
            )

            cursor.execute("""
                INSERT INTO simulation_assignments
                (ticket_id, agent_id, priority, status, routing_reason)
                VALUES (?, ?, ?, 'Active', ?)
            """, (
                ticket_id,
                selected_agent,
                priority,
                "Skill, language and capacity matched"
            ))

            # Mark as simulated, not actually assigned
            cursor.execute("""
                UPDATE overflow_queue
                SET status = 'Simulated'
                WHERE ticket_id = ?
                  AND status = 'Waiting'
            """, (ticket_id,))

            agents[selected_agent]["workload"] += 1
            assigned_count += 1

        conn.commit()

        print("\n--- CAPACITY-AWARE ROUTING RESULTS ---")
        print("Tickets checked:", len(tickets))
        print("Simulation assignments created:", assigned_count)
        print("Tickets still waiting:", waiting_count)

        print("\n--- AGENT SIMULATION WORKLOAD ---")

        for agent_id, details in sorted(agents.items()):
            print(
                f"{agent_id} | "
                f"Workload: {details['workload']} | "
                f"Capacity: {details['capacity']} | "
                f"Available: {max(0, details['capacity'] - details['workload'])}"
            )

        print("\nOriginal tickets and assignment history were not changed.")
        print("Simulation completed successfully.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    run_simulation()
