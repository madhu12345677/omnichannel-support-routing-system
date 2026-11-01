
import sqlite3

DB_PATH = "database/support_system.db"
SIMULATION_CAPACITY = 8

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

PRIORITY_ORDER = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4
}


def populate_overflow_queue():
    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT t.ticket_id, i.intent_name,
                   t.language_id, t.priority
            FROM tickets t
            JOIN intents i ON t.intent_id = i.intent_id
            WHERE t.status = 'Unassigned'
        """)
        tickets = cursor.fetchall()

        cursor.execute("""
            SELECT agent_id
            FROM agents
            WHERE status = 'Active'
        """)
        agents = [row[0] for row in cursor.fetchall()]

        cursor.execute("""
            SELECT agent_id, skill_id FROM agent_skills
        """)
        agent_skills = {}
        for agent_id, skill_id in cursor.fetchall():
            agent_skills.setdefault(agent_id, set()).add(skill_id)

        cursor.execute("""
            SELECT agent_id, language_id FROM agent_languages
        """)
        agent_languages = {}
        for agent_id, language_id in cursor.fetchall():
            agent_languages.setdefault(agent_id, set()).add(language_id)

        cursor.execute("""
            SELECT skill_id, skill_name FROM skills
        """)
        skill_ids = {
            name: skill_id
            for skill_id, name in cursor.fetchall()
        }

        workload = {agent_id: 0 for agent_id in agents}

        tickets.sort(
            key=lambda ticket: PRIORITY_ORDER.get(ticket[3], 5)
        )

        overflow_tickets = []

        for ticket_id, intent, language_id, priority in tickets:
            required_skill = skill_ids.get(
                INTENT_SKILL_MAP.get(intent)
            )

            candidates = []

            for agent_id in agents:
                if workload[agent_id] >= SIMULATION_CAPACITY:
                    continue

                if required_skill is None:
                    continue

                if required_skill not in agent_skills.get(agent_id, set()):
                    continue

                if language_id not in agent_languages.get(agent_id, set()):
                    continue

                candidates.append(agent_id)

            if candidates:
                selected_agent = min(
                    candidates,
                    key=lambda agent_id: workload[agent_id]
                )
                workload[selected_agent] += 1

            else:
                overflow_tickets.append((ticket_id, priority))

        cursor.executemany("""
            INSERT OR IGNORE INTO overflow_queue
            (ticket_id, priority, reason, status)
            VALUES (?, ?, ?, 'Waiting')
        """, [
            (ticket_id, priority, "Agent capacity full")
            for ticket_id, priority in overflow_tickets
        ])

        conn.commit()

        cursor.execute("""
            SELECT COUNT(*)
            FROM overflow_queue
            WHERE status = 'Waiting'
        """)
        waiting_count = cursor.fetchone()[0]

        print("\nOVERFLOW QUEUE POPULATED SUCCESSFULLY!")
        print("Tickets checked:", len(tickets))
        print("Overflow tickets identified:", len(overflow_tickets))
        print("Total waiting records in database:", waiting_count)

        print("\nExisting ticket statuses and assignments were not changed.")

    except Exception as error:
        conn.rollback()
        print("ERROR:", error)

    finally:
        conn.close()


if __name__ == "__main__":
    populate_overflow_queue()
