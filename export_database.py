import sqlite3
import csv
from pathlib import Path

# Database location
DB_PATH = Path("database/support_system.db")

# CSV export folder
OUTPUT_DIR = Path("data/csv")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def export_tables():
    if not DB_PATH.exists():
        print("ERROR: Database file not found:", DB_PATH)
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all user-created tables
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    tables = [row[0] for row in cursor.fetchall()]

    print("Total tables found:", len(tables))

    for table in tables:
        # Safely quote the table name
        safe_table = table.replace('"', '""')
        cursor.execute(f'SELECT * FROM "{safe_table}"')

        columns = [description[0] for description in cursor.description]

        output_file = OUTPUT_DIR / f"{table}.csv"

        with open(output_file, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(columns)

            row_count = 0

            while True:
                rows = cursor.fetchmany(5000)
                if not rows:
                    break

                writer.writerows(rows)
                row_count += len(rows)

        print(f"Exported: {table}.csv | Records: {row_count}")

    conn.close()

    print("\nCSV EXPORT COMPLETED SUCCESSFULLY!")
    print("Output folder:", OUTPUT_DIR.resolve())

if __name__ == "__main__":
    export_tables()