import sqlite3

DB_PATH = "database/support_system.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

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
    ),
    workloads AS (
        SELECT
            le.agent_id,
            COUNT(*) AS current_workload
        FROM latest_events le
        JOIN tickets t ON le.ticket_id = t.ticket_id
        WHERE le.rn = 1
          AND le.action_type = 'Assigned'
          AND t.status IN ('Assigned', 'In Progress', 'Pending')
        GROUP BY le.agent_id
    )
    SELECT
        a.agent_id,
        a.max_concurrent_tickets,
        COALESCE(w.current_workload, 0),
        MAX(
            0,
            a.max_concurrent_tickets -
            COALESCE(w.current_workload, 0)
        ) AS available_slots
    FROM agents a
    LEFT JOIN workloads w ON a.agent_id = w.agent_id
    WHERE a.status = 'Active'
    ORDER BY available_slots DESC, a.agent_id
""")

print("\n--- ACTIVE AGENT CAPACITY REPORT ---")

for row in cursor.fetchall():
    print(
        f"Agent: {row[0]} | Capacity: {row[1]} | "
        f"Workload: {row[2]} | Available: {row[3]}"
    )

conn.close()

print("\nREAD-ONLY CHECK COMPLETED.")