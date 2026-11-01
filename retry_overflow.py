
import sqlite3

DB_PATH = "database/support_system.db"

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


def retry_overflow():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    agent_id = input("Enter available Agent ID (example A094): ").strip()

    cursor.execute("""
        SELECT agent_id, status
        FROM agents
        WHERE agent_id = ?
    """, (agent_id,))

    agent = cursor.fetchone()

    if not agent or agent[1] != "Active":
        print("Agent not found or not active.")
        conn.close()
        return

    cursor.execute("""
        SELECT skill_id
        FROM agent_skills
        WHERE agent_id = ?
    """, (agent_id,))
    agent_skills = {row[0] for row in cursor.fetchall()}

    cursor.execute("""
        SELECT language_id
        FROM agent_languages
        WHERE agent_id = ?
    """, (agent_id,))
    agent_languages = {row[0] for row in cursor.fetchall()}

    cursor.execute("""
        SELECT skill_id, skill_name
        FROM skills
    """)
    skill_ids = {
        name: skill_id
        for skill_id, name in cursor.fetchall()
    }

    cursor.execute("""
        SELECT oq.ticket_id, oq.priority,
               t.language_id, i.intent_name
        FROM overflow_queue oq
        JOIN tickets t ON oq.ticket_id = t.ticket_id
        JOIN intents i ON t.intent_id = i.intent_id
        WHERE oq.status = 'Waiting'
    """)
    waiting_tickets = cursor.fetchall()

    waiting_tickets.sort(
        key=lambda ticket: PRIORITY_ORDER.get(ticket[1], 5)
    )

    selected_ticket = None

    for ticket_id, priority, language_id, intent in waiting_tickets:
        required_skill = skill_ids.get(
            INTENT_SKILL_MAP.get(intent)
        )

        if required_skill is None:
            continue

        if required_skill not in agent_skills:
            continue

        if language_id not in agent_languages:
            continue

        selected_ticket = (ticket_id, priority, intent)
        break

    print("\n--- AUTOMATIC REASSIGNMENT PREVIEW ---")
    print("Agent:", agent_id)

    if selected_ticket:
        ticket_id, priority, intent = selected_ticket

        print("Suitable waiting ticket found!")
        print("Ticket ID:", ticket_id)
        print("Priority:", priority)
        print("Intent:", intent)
        print("Skill match: Yes")
        print("Language match: Yes")
        print("Simulation: One available slot used.")
    else:
        print("No matching waiting ticket found for this agent.")

    print("\nDRY RUN: No database records were changed.")

    conn.close()


if __name__ == "__main__":
    retry_overflow()
