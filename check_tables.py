import sqlite3

conn = sqlite3.connect("database/support_system.db")
cursor = conn.cursor()

tables = cursor.execute("""
SELECT name FROM sqlite_master
WHERE type='table'
""").fetchall()

for table in tables:
    name = table[0]
    count = cursor.execute(
        f'SELECT COUNT(*) FROM "{name}"'
    ).fetchone()[0]

    print(f"{name}: {count} records")

conn.close()