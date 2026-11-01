
import sqlite3

DB_PATH = "database/support_system.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS overflow_queue (
        overflow_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT NOT NULL UNIQUE,
        priority TEXT NOT NULL,
        reason TEXT DEFAULT 'Agent capacity full',
        status TEXT NOT NULL DEFAULT 'Waiting',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
    )
""")

conn.commit()

print("OVERFLOW QUEUE TABLE CREATED SUCCESSFULLY!")

cursor.execute("PRAGMA table_info(overflow_queue)")
columns = cursor.fetchall()

print("\n--- OVERFLOW QUEUE TABLE COLUMNS ---")
for column in columns:
    print(column[1], "-", column[2])

cursor.execute("SELECT COUNT(*) FROM overflow_queue")
print("\nCurrent overflow records:", cursor.fetchone()[0])

conn.close()

print("\nExisting ticket records were not modified.")
