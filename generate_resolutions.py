
import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "database/support_system.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

try:
    tickets = cursor.execute("""
        SELECT ticket_id, status, created_at
        FROM tickets
    """).fetchall()

    if not tickets:
        raise Exception("No tickets found.")

    resolutions = []

    resolution_number = 1

    resolution_notes_list = [
        "Customer issue resolved successfully.",
        "Provided the required information to the customer.",
        "Technical issue fixed by the support team.",
        "Customer request completed successfully.",
        "Issue investigated and solution provided."
    ]

    for ticket_id, status, created_at in tickets:

        # Only resolved or closed tickets get resolution records
        if status not in ["Resolved", "Closed"]:
            continue

        created_time = datetime.strptime(
            created_at, "%Y-%m-%d %H:%M:%S"
        )

        resolved_time = created_time + timedelta(
            hours=random.randint(1, 48)
        )

        resolution_status = random.choices(
            ["Resolved", "Rejected"],
            weights=[95, 5]
        )[0]

        resolution_notes = random.choice(
            resolution_notes_list
        )

        # Customer satisfaction score from 1 to 5
        satisfaction = random.randint(3, 5)

        resolution_id = f"RES{resolution_number:06d}"

        resolutions.append((
            resolution_id,
            ticket_id,
            resolution_status,
            resolution_notes,
            resolved_time.strftime("%Y-%m-%d %H:%M:%S"),
            satisfaction
        ))

        resolution_number += 1

    cursor.executemany("""
        INSERT OR IGNORE INTO resolutions (
            resolution_id,
            ticket_id,
            resolution_status,
            resolution_notes,
            resolved_at,
            customer_satisfaction
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, resolutions)

    conn.commit()

    total = cursor.execute(
        "SELECT COUNT(*) FROM resolutions"
    ).fetchone()[0]

    print("RESOLUTIONS GENERATED SUCCESSFULLY!")
    print("Resolution records attempted:", len(resolutions))
    print("Total resolutions in database:", total)

except Exception as e:
    conn.rollback()
    print("ERROR:", e)

finally:
    conn.close()
