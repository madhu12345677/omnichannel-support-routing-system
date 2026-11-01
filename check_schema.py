import sqlite3

conn = sqlite3.connect("database/support_system.db")

tables = conn.execute("""
SELECT COUNT(*)
FROM sqlite_master
WHERE type = 'table'
""").fetchone()[0]

indexes = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'index'
AND name NOT LIKE 'sqlite_%'
""").fetchall()

print("Total tables:", tables)
print("Indexes:", indexes)

conn.close()