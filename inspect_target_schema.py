import sqlite3

db_path = "database/support_system.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    SELECT name, sql
    FROM sqlite_master
    WHERE type = 'table'
    AND name NOT LIKE 'sqlite_%'
    ORDER BY name
""")

for table_name, create_sql in cursor.fetchall():
    print("\n" + "=" * 60)
    print("TABLE:", table_name)
    print("=" * 60)
    print(create_sql)

conn.close()