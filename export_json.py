import sqlite3
import json
from pathlib import Path

DB_PATH = Path("database/support_system.db")
OUTPUT_DIR = Path("data/json")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def export_json():
    if not DB_PATH.exists():
        print("ERROR: Database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    tables = [row["name"] for row in cursor.fetchall()]

    print("Total project tables:", len(tables))

    for table in tables:
        safe_table = table.replace('"', '""')
        cursor.execute(f'SELECT * FROM "{safe_table}"')

        records = [dict(row) for row in cursor.fetchall()]

        output_file = OUTPUT_DIR / f"{table}.json"

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(
                records,
                file,
                indent=4,
                ensure_ascii=False,
                default=str
            )

        print(f"Exported: {table}.json | Records: {len(records)}")

    conn.close()

    print("\nJSON EXPORT COMPLETED!")
    print("Output folder:", OUTPUT_DIR.resolve())


if __name__ == "__main__":
    export_json()