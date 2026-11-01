import sqlite3

conn = sqlite3.connect("database/support_system.db")

result = conn.execute("""
SELECT sql
FROM sqlite_master
WHERE type = 'table'
AND name = 'tickets'
""").fetchone()

print(result[0])

conn.close()