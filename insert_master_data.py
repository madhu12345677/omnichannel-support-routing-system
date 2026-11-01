
import sqlite3
import csv
from datetime import datetime

DB_PATH = "database/support_system.db"
TODAY = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def read_csv(filename):
    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

try:
    # 1. Channels
    channels = read_csv("channels.csv")
    channel_ids = {}

    for i, row in enumerate(channels, 1):
        cid = f"CH{i:03d}"
        name = row["channel_name"]
        channel_ids[name] = cid

        cursor.execute("""
            INSERT OR IGNORE INTO channels
            (channel_id, channel_name, calendar_type,
             business_start, business_end, timezone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (cid, name, "BUSINESS_HOURS",
              "09:00", "18:00", "Asia/Kolkata"))

    # 2. Languages
    languages = read_csv("languages.csv")
    language_ids = {}

    for i, row in enumerate(languages, 1):
        lid = f"L{i:03d}"
        name = row["language_name"]
        language_ids[name] = lid

        cursor.execute("""
            INSERT OR IGNORE INTO languages
            VALUES (?, ?, ?)
        """, (lid, name, f"lang{i:03d}"))

    # 3. Intents
    intents = read_csv("intents.csv")
    intent_ids = {}

    priorities = ["High", "Medium", "High", "Critical",
                   "Low", "High", "Medium", "High"]

    for i, row in enumerate(intents, 1):
        iid = f"I{i:03d}"
        name = row["intent_name"]
        priority = priorities[i - 1]
        intent_ids[name] = (iid, priority)

        cursor.execute("""
            INSERT OR IGNORE INTO intents
            (intent_id, intent_name, description,
             default_priority, active)
            VALUES (?, ?, ?, ?, ?)
        """, (iid, name, f"Support for {name}",
              priority, 1))

    # 4. Skills
    skills = read_csv("skills.csv")
    skill_ids = {}

    for i, row in enumerate(skills, 1):
        sid = f"SK{i:03d}"
        name = row["skill_name"]
        skill_ids[name] = sid

        cursor.execute("""
            INSERT OR IGNORE INTO skills
            VALUES (?, ?, ?)
        """, (sid, name, f"{name} support skill"))

    # 5. Queues
    queues = read_csv("queues.csv")
    queue_ids = {}

    for i, row in enumerate(queues, 1):
        qid = f"Q{i:03d}"
        name = row["queue_name"]
        queue_ids[name] = qid

        cursor.execute("""
            INSERT OR IGNORE INTO queues
            VALUES (?, ?, ?, ?)
        """, (qid, name, f"{name} handling queue", 1))

    # 6. Customers
    customers = read_csv("customers.csv")

    for row in customers:
        cid = f"C{int(row['customer_id']):05d}"
        language_id = language_ids[row["language"]]

        cursor.execute("""
            INSERT OR IGNORE INTO customers
            (customer_id, customer_name, email, phone,
             preferred_language_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (cid, row["customer_name"], row["email"],
              row["phone"], language_id, TODAY))

    # 7. Agents
    agents = read_csv("agents.csv")

    for row in agents:
        aid = f"A{int(row['agent_id']):03d}"

        status_map = {
            "Available": "Active",
            "Busy": "Active",
            "Offline": "Inactive"
        }

        cursor.execute("""
            INSERT OR IGNORE INTO agents
            (agent_id, agent_name, email, status,
             shift_start, shift_end, max_concurrent_tickets)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (aid, row["agent_name"], row["email"],
              status_map.get(row["status"], "Active"),
              "09:00", "18:00", 5))

        # Agent skill mapping
        sid = skill_ids[row["skill"]]

        cursor.execute("""
            INSERT OR IGNORE INTO agent_skills
            VALUES (?, ?, ?, ?, ?)
        """, (aid, sid, "Intermediate", TODAY, None))

        # Agent language mapping
        lid = language_ids[row["language"]]

        cursor.execute("""
            INSERT OR IGNORE INTO agent_languages
            VALUES (?, ?, ?, ?, ?)
        """, (aid, lid, "Fluent", TODAY, None))

    # 8. Priority and SLA rules
    sla_times = {
        "Critical": (5, 60),
        "High": (15, 240),
        "Medium": (60, 480),
        "Low": (240, 1440)
    }

    for i, row in enumerate(intents, 1):
        iid, priority = intent_ids[row["intent_name"]]
        response, resolution = sla_times[priority]

        cursor.execute("""
            INSERT OR IGNORE INTO priority_rules
            (rule_id, intent_id, channel_id, priority,
             first_response_minutes, resolution_minutes,
             effective_from, effective_to)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (f"PR{i:03d}", iid, None, priority,
              response, resolution, TODAY, None))

    conn.commit()

    print("MASTER DATA INSERTED SUCCESSFULLY!")
    for table in [
        "channels", "languages", "intents", "skills",
        "queues", "customers", "agents",
        "agent_skills", "agent_languages", "priority_rules"
    ]:
        count = cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]
        print(f"{table}: {count}")

except Exception as error:
    conn.rollback()
    print("ERROR:", error)

finally:
    conn.close()
