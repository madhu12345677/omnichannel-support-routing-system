
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "support_system.db"

connection = sqlite3.connect(DB_PATH)

# Enable foreign key validation
connection.execute("PRAGMA foreign_keys = ON")

# Get all tables
tables = connection.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""").fetchall()

print("DATABASE VERIFICATION")
print("---------------------")

print("Total tables:", len(tables))

for table in tables:
    print("Table:", table[0])

# Check foreign key violations
violations = connection.execute(
    "PRAGMA foreign_key_check"
).fetchall()

if len(violations) == 0:
    print("\nForeign key check: PASSED")
else:
    print("\nForeign key check: FAILED")
    print(violations)

# Check important tables
required_tables = [
    "customers",
    "tickets",
    "messages",
    "agents",
    "intents",
    "assignment_events",
    "sla_events",
    "resolutions"
]

existing_tables = [table[0] for table in tables]

for table in required_tables:
    if table in existing_tables:
        print(f"{table}: EXISTS")
    else:
        print(f"{table}: MISSING")

connection.close()

print("\nDatabase verification completed!")
