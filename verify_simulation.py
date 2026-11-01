import sqlite3

DB_PATH = "database/support_system.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\n--- SIMULATION STATUS SUMMARY ---")

cursor.execute("""
    SELECT status, COUNT(*)
    FROM simulation_assignments
    GROUP BY status
""")

for row in cursor.fetchall():
    print(row)

print("\n--- OVERFLOW QUEUE SUMMARY ---")

cursor.execute("""
    SELECT status, COUNT(*)
    FROM overflow_queue
    GROUP BY status
""")

for row in cursor.fetchall():
    print(row)

print("\n--- AGENT CAPACITY VALIDATION ---")

cursor.execute("""
    SELECT sa.agent_id,
           COUNT(*) AS workload,
           a.max_concurrent_tickets
    FROM simulation_assignments sa
    JOIN agents a ON sa.agent_id = a.agent_id
    WHERE sa.status = 'Active'
    GROUP BY sa.agent_id
    HAVING COUNT(*) > a.max_concurrent_tickets
""")

overloaded = cursor.fetchall()

if overloaded:
    print("Capacity violations found:", overloaded)
else:
    print("PASS: No agent exceeded capacity.")

print("\n--- DUPLICATE TICKET CHECK ---")

cursor.execute("""
    SELECT ticket_id, COUNT(*)
    FROM simulation_assignments
    GROUP BY ticket_id
    HAVING COUNT(*) > 1
""")

duplicates = cursor.fetchall()

if duplicates:
    print("Duplicates found:", duplicates)
else:
    print("PASS: No duplicate simulation assignments.")

cursor.execute("""
    SELECT COUNT(*)
    FROM simulation_assignments
""")

print("\nTotal simulation assignments:", cursor.fetchone()[0])

conn.close()

print("\nVERIFICATION COMPLETED.")