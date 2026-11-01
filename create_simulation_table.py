import sqlite3

DB_PATH = "database/support_system.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS simulation_assignments (
        simulation_assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT NOT NULL UNIQUE,
        agent_id TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Active',
        assigned_at TEXT DEFAULT CURRENT_TIMESTAMP,
        routing_reason TEXT,
        FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
        FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
    )
""")

conn.commit()

print("SIMULATION ASSIGNMENTS TABLE CREATED!")

cursor.execute("PRAGMA table_info(simulation_assignments)")

print("\n--- TABLE COLUMNS ---")
for column in cursor.fetchall():
    print(column[1], "-", column[2])

cursor.execute("SELECT COUNT(*) FROM simulation_assignments")
print("\nCurrent simulation assignments:", cursor.fetchone()[0])

conn.close()

print("\nExisting assignment history was not modified.")