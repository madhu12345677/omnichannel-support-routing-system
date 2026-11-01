import sqlite3

DB_PATH = "database/support_system.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\n--- ASSIGNMENT ACTION TYPES ---")
cursor.execute("""
    SELECT action_type, COUNT(*)
    FROM assignment_events
    GROUP BY action_type
""")
for row in cursor.fetchall():
    print(row)

print("\n--- TICKET STATUS COUNTS ---")
cursor.execute("""
    SELECT status, COUNT(*)
    FROM tickets
    GROUP BY status
""")
for row in cursor.fetchall():
    print(row)

print("\n--- AGENT A095 DETAILS ---")
cursor.execute("""
    SELECT agent_id, status, max_concurrent_tickets
    FROM agents
    WHERE agent_id = 'A095'
""")
print(cursor.fetchone())

print("\n--- A095 ASSIGNMENT HISTORY ---")
cursor.execute("""
    SELECT action_type, COUNT(*)
    FROM assignment_events
    WHERE agent_id = 'A095'
    GROUP BY action_type
""")
for row in cursor.fetchall():
    print(row)

print("\n--- TICKET TKT002024 DETAILS ---")
cursor.execute("""
    SELECT ticket_id, status, priority
    FROM tickets
    WHERE ticket_id = 'TKT002024'
""")
print(cursor.fetchone())

print("\n--- TICKET TKT002024 ASSIGNMENT HISTORY ---")
cursor.execute("""
    SELECT assignment_id, agent_id, action_type, event_time
    FROM assignment_events
    WHERE ticket_id = 'TKT002024'
    ORDER BY event_time
""")
for row in cursor.fetchall():
    print(row)

conn.close()

print("\nREAD-ONLY CHECK COMPLETED. No database records changed.")