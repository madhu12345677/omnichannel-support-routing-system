
import sqlite3

DB_PATH = "database/support_system.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("DATABASE QUALITY VALIDATION")
print("=" * 40)

# 1. Check duplicate primary IDs
tables = [
    "customers",
    "agents",
    "tickets",
    "messages",
    "assignment_events",
    "sla_events",
    "resolutions"
]

print("\n1. DUPLICATE ID CHECK")

for table in tables:
    primary_key = {
        "customers": "customer_id",
        "agents": "agent_id",
        "tickets": "ticket_id",
        "messages": "message_id",
        "assignment_events": "assignment_id",
        "sla_events": "sla_event_id",
        "resolutions": "resolution_id"
    }[table]

    cursor.execute(f"""
        SELECT COUNT(*) - COUNT(DISTINCT {primary_key})
        FROM {table}
    """)

    duplicates = cursor.fetchone()[0]
    print(f"{table}: {duplicates} duplicate IDs")

# 2. Check foreign key violations
print("\n2. FOREIGN KEY CHECK")

cursor.execute("PRAGMA foreign_key_check")
fk_errors = cursor.fetchall()

if fk_errors:
    print("Foreign key issues found:", len(fk_errors))
    for error in fk_errors[:10]:
        print(error)
else:
    print("No foreign key violations found.")

# 3. Check NULL values in important columns
print("\n3. IMPORTANT NULL CHECK")

checks = {
    "customers": ["customer_id"],
    "agents": ["agent_id"],
    "tickets": ["ticket_id", "customer_id", "created_at"],
    "messages": ["message_id", "ticket_id", "message_text"],
    "assignment_events": ["assignment_id", "ticket_id", "event_time"],
    "sla_events": ["sla_event_id", "ticket_id", "event_time"],
    "resolutions": ["resolution_id", "ticket_id", "resolved_at"]
}

for table, columns in checks.items():
    for column in columns:
        cursor.execute(
            f"SELECT COUNT(*) FROM {table} WHERE {column} IS NULL"
        )
        null_count = cursor.fetchone()[0]
        print(f"{table}.{column}: {null_count} NULL values")

conn.close()

print("\nDATABASE VALIDATION COMPLETED!")
