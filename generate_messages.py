
import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "database/support_system.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

try:
    tickets = cursor.execute("""
        SELECT ticket_id, customer_id, created_at
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

    customer_messages = [
        "Hello, I need help with my issue.",
        "I am facing a problem with this service.",
        "Could you please check this issue?",
        "I need assistance regarding my recent request.",
        "Please help me resolve this problem."
    ]

    agent_messages = [
        "Hello! Thank you for contacting support. I will help you.",
        "I understand your concern. Let me check the details.",
        "Thank you for sharing the information. We are checking it.",
        "We are working on your request. Thank you for your patience.",
        "Your concern has been reviewed. Please let us know if you need further help."
    ]

    messages = []
    message_number = 1

    for ticket_id, customer_id, created_at in tickets:

        agent_id = random.choice(agents)[0]

        base_time = datetime.strptime(
            created_at, "%Y-%m-%d %H:%M:%S"
        )

        conversation = [
            ("Customer", customer_id, None,
             random.choice(customer_messages)),
            ("Agent", None, agent_id,
             random.choice(agent_messages)),
            ("Customer", customer_id, None,
             random.choice(customer_messages)),
            ("Agent", None, agent_id,
             random.choice(agent_messages))
        ]

        for sequence, (sender_type, customer, agent, message_text) in enumerate(
            conversation, start=1
        ):
            sent_at = base_time + timedelta(minutes=sequence * 5)

            message_id = f"MSG{message_number:07d}"

            messages.append((
                message_id,
                ticket_id,
                sequence,
                sender_type,
                customer,
                agent,
                message_text,
                sent_at.strftime("%Y-%m-%d %H:%M:%S")
            ))

            message_number += 1

    cursor.executemany("""
        INSERT OR IGNORE INTO messages (
            message_id,
            ticket_id,
            sequence_number,
            sender_type,
            sender_customer_id,
            sender_agent_id,
            message_text,
            sent_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, messages)

    conn.commit()

    total = cursor.execute(
        "SELECT COUNT(*) FROM messages"
    ).fetchone()[0]

    print("MESSAGES GENERATED SUCCESSFULLY!")
    print("Messages attempted:", len(messages))
    print("Total messages in database:", total)

except Exception as e:
    conn.rollback()
    print("ERROR:", e)

finally:
    conn.close()
