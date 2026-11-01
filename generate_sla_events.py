
import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "database/support_system.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

try:
    tickets = cursor.execute("""
        SELECT
            t.ticket_id,
            t.created_at,
            t.priority,
            MIN(
                CASE
                    WHEN m.sender_type = 'Agent'
                    THEN m.sent_at
                END
            ) AS first_response
        FROM tickets t
        LEFT JOIN messages m
            ON t.ticket_id = m.ticket_id
        GROUP BY t.ticket_id
    """).fetchall()

    if not tickets:
        raise Exception("No tickets found.")

    response_targets = {
        "Critical": 5,
        "High": 15,
        "Medium": 60,
        "Low": 240
    }

    events = []
    event_number = 1

    for ticket_id, created_at, priority, first_response in tickets:

        start_time = datetime.strptime(
            created_at, "%Y-%m-%d %H:%M:%S"
        )

        response_minutes = response_targets.get(priority, 60)

        target_time = start_time + timedelta(
            minutes=response_minutes
        )

        # SLA Started event
        events.append((
            f"SLA{event_number:07d}",
            ticket_id,
            "Started",
            target_time.strftime("%Y-%m-%d %H:%M:%S"),
            None,
            start_time.strftime("%Y-%m-%d %H:%M:%S")
        ))
        event_number += 1

        # First response event
        if first_response:
            actual_response = datetime.strptime(
                first_response, "%Y-%m-%d %H:%M:%S"
            )

            response_event_type = "First_Response"

            events.append((
                f"SLA{event_number:07d}",
                ticket_id,
                response_event_type,
                target_time.strftime("%Y-%m-%d %H:%M:%S"),
                actual_response.strftime("%Y-%m-%d %H:%M:%S"),
                actual_response.strftime("%Y-%m-%d %H:%M:%S")
            ))
            event_number += 1

            # Check first response SLA
            if actual_response <= target_time:
                final_event = "Met"
            else:
                final_event = "Breached"

            events.append((
                f"SLA{event_number:07d}",
                ticket_id,
                final_event,
                target_time.strftime("%Y-%m-%d %H:%M:%S"),
                actual_response.strftime("%Y-%m-%d %H:%M:%S"),
                actual_response.strftime("%Y-%m-%d %H:%M:%S")
            ))
            event_number += 1

        else:
            # No agent response found
            events.append((
                f"SLA{event_number:07d}",
                ticket_id,
                "At_Risk",
                target_time.strftime("%Y-%m-%d %H:%M:%S"),
                None,
                start_time.strftime("%Y-%m-%d %H:%M:%S")
            ))
            event_number += 1

    cursor.executemany("""
        INSERT OR IGNORE INTO sla_events (
            sla_event_id,
            ticket_id,
            event_type,
            target_at,
            actual_at,
            event_time
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, events)

    conn.commit()

    total = cursor.execute(
        "SELECT COUNT(*) FROM sla_events"
    ).fetchone()[0]

    print("SLA EVENTS GENERATED SUCCESSFULLY!")
    print("Events attempted:", len(events))
    print("Total SLA events:", total)

except Exception as e:
    conn.rollback()
    print("ERROR:", e)

finally:
    conn.close()
