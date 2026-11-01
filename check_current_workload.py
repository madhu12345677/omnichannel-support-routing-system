import sqlite3

DB_PATH = "database/support_system.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\n--- A095: LATEST ASSIGNMENT RECORDS ---")

cursor.execute("""
    WITH latest_events AS (
        SELECT
            ticket_id,
            agent_id,
            action_type,
            ROW_NUMBER() OVER (
                PARTITION BY ticket_id
                ORDER BY event_time DESC, assignment_id DESC
            ) AS rn
        FROM assignment_events
    )
    SELECT
        t.status,
        COUNT(*)
    FROM latest_events le
    JOIN tickets t ON le.ticket_id = t.ticket_id
    WHERE le.rn = 1
      AND le.agent_id = 'A095'
      AND le.action_type = 'Assigned'
    GROUP BY t.status
""")

for row in cursor.fetchall():
    print(row)

print("\n--- A095: CURRENT ASSIGNED TICKETS ---")

cursor.execute("""
    WITH latest_events AS (
        SELECT
            ticket_id,
            agent_id,
            action_type,
            ROW_NUMBER() OVER (
                PARTITION BY ticket_id
                ORDER BY event_time DESC, assignment_id DESC
            ) AS rn
        FROM assignment_events
    )
    SELECT
        le.ticket_id,
        t.status
    FROM latest_events le
    JOIN tickets t ON le.ticket_id = t.ticket_id
    WHERE le.rn = 1
      AND le.agent_id = 'A095'
      AND le.action_type = 'Assigned'
      AND t.status IN ('Assigned', 'In Progress', 'Pending')
""")

current_tickets = cursor.fetchall()

for ticket in current_tickets:
    print(ticket)

print("\nCurrent workload:", len(current_tickets))

cursor.execute("""
    SELECT max_concurrent_tickets
    FROM agents
    WHERE agent_id = 'A095'
""")

capacity = cursor.fetchone()[0]

print("Maximum capacity:", capacity)
print("Available slots:", max(0, capacity - len(current_tickets)))

conn.close()

print("\nREAD-ONLY CHECK COMPLETED. No database records changed.")