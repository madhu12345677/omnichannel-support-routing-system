import sqlite3

conn = sqlite3.connect("database/support_system.db")

query = """
SELECT COUNT(*)
FROM overflow_queue o
JOIN simulation_assignments s
ON o.ticket_id = s.ticket_id
WHERE o.status = 'Waiting'
"""

result = conn.execute(query).fetchone()

print("Waiting tickets already assigned:", result[0])

conn.close()