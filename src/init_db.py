
import sqlite3
from pathlib import Path

# Project folder location
BASE_DIR = Path(__file__).resolve().parent.parent

# Database and schema paths
DB_PATH = BASE_DIR / "database" / "support_system.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

# Create database
connection = sqlite3.connect(DB_PATH)

# Enable foreign key validation
connection.execute("PRAGMA foreign_keys = ON")

# Read SQL schema
with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
    schema = file.read()

# Create all tables
connection.executescript(schema)

# Verify tables
tables = connection.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""").fetchall()

print("Database created successfully!")
print("\nTables created:")

for table in tables:
    print("-", table[0])

connection.close()
