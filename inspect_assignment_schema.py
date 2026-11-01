import sqlite3

DB_PATH = "database/support_system.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

tables = ["assignment_events", "tickets", "agents", "overflow_queue"]

for table in tables:
    print(f"\n--- {table.upper()} TABLE ---")

    cursor.execute(f"PRAGMA table_info({table})")

    for column in cursor.fetchall():
        print(column)

conn.close()