
import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "database/support_system.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

try:
    # Fetch customers with their preferred languages
    customers = cursor.execute("""
        SELECT customer_id, preferred_language_id
        FROM customers
    """).fetchall()

    channels = cursor.execute("""
        SELECT channel_id FROM channels
    """).fetchall()

    intents = cursor.execute("""
        SELECT intent_id, default_priority
        FROM intents
        WHERE active = 1
    """).fetchall()

    queues = cursor.execute("""
        SELECT queue_id FROM queues
        WHERE active = 1
    """).fetchall()

    rules = cursor.execute("""
        SELECT rule_id, intent_id, priority
        FROM priority_rules
    """).fetchall()

    if not customers or not channels or not intents or not queues:
        raise Exception("Required master data is missing.")

    # Match priority rules with intents
    rule_map = {}
    for rule_id, intent_id, priority in rules:
        rule_map[intent_id] = (rule_id, priority)

    statuses = [
        "New", "Open", "Assigned", "In Progress",
        "Pending", "Resolved", "Closed", "Reopened",
        "Unassigned"
    ]

    ticket_count = 5000

    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 10, 30)

    total_days = (end_date - start_date).days
    tickets = []

    for i in range(1, ticket_count + 1):

        ticket_id = f"TKT{i:06d}"

        customer_id, language_id = random.choice(customers)
        channel_id = random.choice(channels)[0]

        intent_id, default_priority = random.choice(intents)

        queue_id = random.choice(queues)[0]

        # Get matching priority rule
        rule_id = None
        priority = default_priority

        if intent_id in rule_map:
            rule_id, priority = rule_map[intent_id]

        # Generate ticket dates
        created_at = start_date + timedelta(
            days=random.randint(0, total_days),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        updated_at = created_at + timedelta(
            hours=random.randint(0, 48)
        )

        if updated_at > end_date:
            updated_at = end_date

        status = random.choice(statuses)

        subject = f"Customer support request - {intent_id}"
        description = (
            f"Customer contacted support regarding {intent_id}."
        )

        tickets.append((
            ticket_id,
            customer_id,
            channel_id,
            intent_id,
            language_id,
            queue_id,
            rule_id,
            subject,
            description,
            priority,
            status,
            created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at.strftime("%Y-%m-%d %H:%M:%S")
        ))

    cursor.executemany("""
        INSERT OR IGNORE INTO tickets (
            ticket_id,
            customer_id,
            channel_id,
            intent_id,
            language_id,
            queue_id,
            rule_id,
            subject,
            description,
            priority,
            status,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tickets)

    conn.commit()

    total = cursor.execute(
        "SELECT COUNT(*) FROM tickets"
    ).fetchone()[0]

    print("TICKETS GENERATED SUCCESSFULLY!")
    print("New tickets attempted:", ticket_count)
    print("Total tickets in database:", total)

except Exception as e:
    conn.rollback()
    print("ERROR:", e)

finally:
    conn.close()
