
import sqlite3

DB_PATH = "database/support_system.db"

# Simulation capacity only. Database capacity remains unchanged.
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


def run_routing_preview():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.ticket_id, i.intent_name, t.language_id, t.priority
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

    cursor.execute("SELECT agent_id, skill_id FROM agent_skills")
    agent_skills = {}
    for agent_id, skill_id in cursor.fetchall():
        agent_skills.setdefault(agent_id, set()).add(skill_id)

    cursor.execute("SELECT agent_id, language_id FROM agent_languages")
    agent_languages = {}
    for agent_id, language_id in cursor.fetchall():
        agent_languages.setdefault(agent_id, set()).add(language_id)

    cursor.execute("SELECT skill_id, skill_name FROM skills")
    skill_ids = {name: skill_id for skill_id, name in cursor.fetchall()}

    # Fresh simulation workload
    new_workload = {agent_id: 0 for agent_id in agents}

    priority_order = {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4
    }

    tickets.sort(key=lambda ticket: priority_order.get(ticket[3], 5))

    assignments = []
    overflow_tickets = []

    skill_missing = 0
    language_missing = 0
    both_missing = 0

    for ticket_id, intent, language_id, priority in tickets:
        required_skill = skill_ids.get(INTENT_SKILL_MAP.get(intent))

        candidates = []

        for agent_id in agents:
            if new_workload[agent_id] >= SIMULATION_CAPACITY:
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
                key=lambda agent_id: new_workload[agent_id]
            )

            new_workload[selected_agent] += 1
            assignments.append((ticket_id, selected_agent))

        else:
            has_skill = any(
                required_skill is not None
                and required_skill in agent_skills.get(agent_id, set())
                for agent_id in agents
            )

            has_language = any(
                language_id in agent_languages.get(agent_id, set())
                for agent_id in agents
            )

            if not has_skill and not has_language:
                both_missing += 1
            elif not has_skill:
                skill_missing += 1
            elif not has_language:
                language_missing += 1

            # Keep the ticket in the virtual overflow queue
            overflow_tickets.append(
                (ticket_id, intent, priority)
            )

    print("\nSAFE ROUTING SIMULATION COMPLETED")
    print("Tickets checked:", len(tickets))
    print("Suitable assignments:", len(assignments))
    print("Overflow queue tickets:", len(overflow_tickets))

    print("\n--- OVERFLOW QUEUE ---")
    print("Status: WAITING FOR AGENT")
    for ticket_id, intent, priority in overflow_tickets[:20]:
        print(
            ticket_id,
            "| Intent:", intent,
            "| Priority:", priority
        )

    if len(overflow_tickets) > 20:
        print("And", len(overflow_tickets) - 20, "more tickets")

    print("\n--- AGENT SIMULATION WORKLOAD ---")
    for agent_id, count in new_workload.items():
        if count > 0:
            print(agent_id, ":", count)

    print("\n--- MATCHING DIAGNOSTICS ---")
    print("Skill not available:", skill_missing)
    print("Language not available:", language_missing)
    print("Both missing:", both_missing)

    print("\nDRY RUN: No database records were changed.")

    conn.close()


if __name__ == "__main__":
    run_routing_preview()
