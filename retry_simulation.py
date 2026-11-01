
import sqlite3

DB_PATH = "database/support_system.db"
AGENT_ID = "A095"

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
    "Complaint": "Complaints"
}


def retry_simulation():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    try:
        cursor.execute("BEGIN IMMEDIATE")

        # Verify agent
        cursor.execute("""
            SELECT status, max_concurrent_tickets
            FROM agents
            WHERE agent_id = ?
        """, (AGENT_ID,))

        agent = cursor.fetchone()

        if not agent or agent[0] != "Active":
            raise Exception("Agent not found or inactive.")

        capacity = agent[1]

        # Find one active simulation ticket
        cursor.execute("""
            SELECT simulation_assignment_id, ticket_id
            FROM simulation_assignments
            WHERE agent_id = ?
              AND status = 'Active'
            ORDER BY assigned_at, simulation_assignment_id
            LIMIT 1
        """, (AGENT_ID,))

        completed = cursor.fetchone()

        if not completed:
            raise Exception("No active simulation ticket to complete.")

        assignment_id, completed_ticket = completed

        # Complete only the simulation assignment
        cursor.execute("""
            UPDATE simulation_assignments
            SET status = 'Completed'
            WHERE simulation_assignment_id = ?
              AND status = 'Active'
        """, (assignment_id,))

        if cursor.rowcount != 1:
            raise Exception("Could not complete simulation assignment.")

        print("\n--- SIMULATED TICKET COMPLETION ---")
        print("Agent:", AGENT_ID)
        print("Completed ticket:", completed_ticket)

        # Calculate current simulation workload
        cursor.execute("""
            SELECT COUNT(*)
            FROM simulation_assignments
            WHERE agent_id = ?
              AND status = 'Active'
        """, (AGENT_ID,))

        workload = cursor.fetchone()[0]
        available = capacity - workload

        print("Current workload:", workload)
        print("Available slots:", available)

        if available <= 0:
            print("No available capacity.")
            conn.commit()
            return

        # Get agent skills and languages
        cursor.execute("""
            SELECT skill_id FROM agent_skills
            WHERE agent_id = ?
        """, (AGENT_ID,))
        agent_skills = {row[0] for row in cursor.fetchall()}

        cursor.execute("""
            SELECT language_id FROM agent_languages
            WHERE agent_id = ?
        """, (AGENT_ID,))
        agent_languages = {row[0] for row in cursor.fetchall()}

        cursor.execute("""
            SELECT skill_id, skill_name FROM skills
        """)
        skill_ids = {
            name: skill_id
            for skill_id, name in cursor.fetchall()
        }

        # Get waiting tickets
        cursor.execute("""
            SELECT oq.ticket_id, oq.priority,
                   t.language_id, i.intent_name
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

        waiting = cursor.fetchall()
        waiting.sort(
            key=lambda row: PRIORITY_ORDER.get(row[1], 5)
        )

        selected = None

        for ticket_id, priority, language_id, intent in waiting:
            required_skill = skill_ids.get(
                INTENT_SKILL_MAP.get(intent)
            )

            if required_skill is None:
                continue

            if required_skill not in agent_skills:
                continue

            if language_id not in agent_languages:
                continue

            selected = (ticket_id, priority, intent)
            break

        if selected:
            ticket_id, priority, intent = selected

            cursor.execute("""
                INSERT INTO simulation_assignments
                (ticket_id, agent_id, priority, status, routing_reason)
                VALUES (?, ?, ?, 'Active', ?)
            """, (
                ticket_id,
                AGENT_ID,
                priority,
                "Automatic retry: skill, language and capacity matched"
            ))

            cursor.execute("""
                UPDATE overflow_queue
                SET status = 'Simulated'
                WHERE ticket_id = ?
                  AND status = 'Waiting'
            """, (ticket_id,))

            if cursor.rowcount != 1:
                raise Exception("Overflow ticket was not updated.")

            print("\n--- AUTOMATIC RETRY RESULT ---")
            print("New ticket:", ticket_id)
            print("Priority:", priority)
            print("Intent:", intent)
            print("Skill match: Yes")
            print("Language match: Yes")
            print("Result: Successfully assigned in simulation.")

        else:
            print("\nNo suitable waiting ticket found for A095.")

        # Final workload
        cursor.execute("""
            SELECT COUNT(*)
            FROM simulation_assignments
            WHERE agent_id = ?
              AND status = 'Active'
        """, (AGENT_ID,))

        final_workload = cursor.fetchone()[0]

        print("\n--- FINAL SIMULATION WORKLOAD ---")
        print("Agent:", AGENT_ID)
        print("Workload:", final_workload)
        print("Capacity:", capacity)
        print("Available:", capacity - final_workload)

        conn.commit()
        print("\nAUTOMATIC RETRY SIMULATION COMPLETED.")

    except Exception as error:
        conn.rollback()
        print("\nERROR:", error)
        print("Changes rolled back.")

    finally:
        conn.close()


if __name__ == "__main__":
    retry_simulation()
