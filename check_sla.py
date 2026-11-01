import sqlite3

conn = sqlite3.connect("database/support_system.db")

query = """
SELECT agent_id, COUNT(*) AS active_tickets
FROM simulation_assignments
WHERE status = 'Active'
GROUP BY agent_id
ORDER BY active_tickets DESC
LIMIT 10
"""

result = conn.execute(query).fetchall()

print("Top 10 agent workloads:")
for row in result:
    print(row)

conn.close()