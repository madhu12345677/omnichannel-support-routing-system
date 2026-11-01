import sqlite3

conn = sqlite3.connect("database/support_system.db")

query = """
SELECT status, COUNT(*)
FROM tickets
WHERE status NOT IN (
    'New', 'Open', 'Assigned', 'In Progress',
    'Pending', 'Resolved', 'Closed', 'Reopened',
    'Unassigned'
)
GROUP BY status
"""

result = conn.execute(query).fetchall()
print("Invalid ticket statuses:", result)

conn.close()