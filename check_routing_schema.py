
import sqlite3

conn = sqlite3.connect("database/support_system.db")
cursor = conn.cursor()

# Check active agents
cursor.execute("""
    SELECT COUNT(*)
    FROM agents
    WHERE status = 'Active'
""")
print("Active agents:", cursor.fetchone()[0])

# Calculate current workload
cursor.execute("""
    SELECT agent_id, COUNT(*)
    FROM assignment_events ae
    JOIN tickets t ON ae.ticket_id = t.ticket_id
    WHERE ae.action_type = 'Assigned'
    AND t.status IN (
        'Assigned', 'In Progress', 'Open',
        'Pending', 'Reopened'
    )
    GROUP BY agent_id
""")

workload = dict(cursor.fetchall())

cursor.execute("""
    SELECT agent_id, agent_name, max_concurrent_tickets
    FROM agents
    WHERE status = 'Active'
""")

agents = cursor.fetchall()

available = 0
print("\n--- AGENT WORKLOAD ---")

for agent_id, name, maximum in agents:
    current = workload.get(agent_id, 0)

    if current < maximum:
        available += 1

    print(
        agent_id,
        name,
        "Current:", current,
        "Maximum:", maximum
    )

print("\nAgents with available capacity:", available)

# Check skill and language matching for sample tickets
cursor.execute("""
    SELECT t.ticket_id, i.intent_name, t.language_id
    FROM tickets t
    JOIN intents i ON t.intent_id = i.intent_id
    WHERE t.status = 'Unassigned'
    LIMIT 5
""")

print("\n--- SAMPLE TICKET MATCHING ---")

for ticket_id, intent, language_id in cursor.fetchall():
    print("\nTicket:", ticket_id)
    print("Intent:", intent)
    print("Language ID:", language_id)

conn.close()
