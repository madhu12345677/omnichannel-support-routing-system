
import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "database/support_system.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

try:
    tickets = cursor.execute("""
        SELECT ticket_id, queue_id, created_at
        FROM tickets
    """).fetchall()

    agents = cursor.execute("""
        SELECT agent_id
        FROM agents
        WHERE status = 'Active'
    """).fetchall()

    if not tickets:
        raise Exception("No tickets found.")

    if not agents:
        raise Exception("No active agents found.")

    events = []

    for i, (ticket_id, queue_id, created_at) in enumerate(
        tickets, start=1
    ):
        event_time = datetime.strptime(
            created_at, "%Y-%m-%d %H:%M:%S"
        ) + timedelta(minutes=random.randint(1, 30))

        # 95% tickets assigned, 5% remain unassigned
        if random.random() < 0.95:
            agent_id = random.choice(agents)[0]
            action_type = "Assigned"
            reason = "Automatically assigned based on queue availability."
        else:
            agent_id = None
            action_type = "Unassigned"
            reason = "Waiting for agent availability."

        assignment_id = f"ASN{i:06d}"

        events.append((
            assignment_id,
            ticket_id,
            agent_id,
            queue_id,
            action_type,
            reason,
            event_time.strftime("%Y-%m-%d %H:%M:%S")
        ))

    cursor.executemany("""
        INSERT OR IGNORE INTO assignment_events (
            assignment_id,
            ticket_id,
            agent_id,
            queue_id,
            action_type,
            routing_reason,
            event_time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, events)

    conn.commit()

    total = cursor.execute(
        "SELECT COUNT(*) FROM assignment_events"
    ).fetchone()[0]

    print("ASSIGNMENT EVENTS GENERATED SUCCESSFULLY!")
    print("Events attempted:", len(events))
    print("Total assignment events:", total)

except Exception as e:
    conn.rollback()
    print("ERROR:", e)

finally:
    conn.close()
