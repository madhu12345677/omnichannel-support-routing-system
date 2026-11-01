
import sqlite3

conn = sqlite3.connect("database/support_system.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT status, COUNT(*)
    FROM overflow_queue
    GROUP BY status
""")

print("OVERFLOW QUEUE STATUS SUMMARY")

for status, count in cursor.fetchall():
    print(status, ":", count)

cursor.execute("""
    SELECT ticket_id, priority, reason, status, created_at
    FROM overflow_queue
    ORDER BY
        CASE priority
            WHEN 'Critical' THEN 1
            WHEN 'High' THEN 2
            WHEN 'Medium' THEN 3
            WHEN 'Low' THEN 4
            ELSE 5
        END
    LIMIT 10
""")

print("\nSAMPLE OVERFLOW TICKETS")

for row in cursor.fetchall():
    print(row)

conn.close()

import sqlite3

conn = sqlite3.connect("database/support_system.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT status, COUNT(*)
    FROM overflow_queue
    GROUP BY status
""")

print("OVERFLOW QUEUE STATUS SUMMARY")

for status, count in cursor.fetchall():
    print(status, ":", count)

cursor.execute("""
    SELECT ticket_id, priority, reason, status, created_at
    FROM overflow_queue
    ORDER BY
        CASE priority
            WHEN 'Critical' THEN 1
            WHEN 'High' THEN 2
            WHEN 'Medium' THEN 3
            WHEN 'Low' THEN 4
            ELSE 5
        END
    LIMIT 10
""")

print("\nSAMPLE OVERFLOW TICKETS")

for row in cursor.fetchall():
    print(row)

conn.close()

import sqlite3

conn = sqlite3.connect("database/support_system.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT status, COUNT(*)
    FROM overflow_queue
    GROUP BY status
""")

print("OVERFLOW QUEUE STATUS SUMMARY")

for status, count in cursor.fetchall():
    print(status, ":", count)

cursor.execute("""
    SELECT ticket_id, priority, reason, status, created_at
    FROM overflow_queue
    ORDER BY
        CASE priority
            WHEN 'Critical' THEN 1
            WHEN 'High' THEN 2
            WHEN 'Medium' THEN 3
            WHEN 'Low' THEN 4
            ELSE 5
        END
    LIMIT 10
""")

print("\nSAMPLE OVERFLOW TICKETS")

for row in cursor.fetchall():
    print(row)

conn.close()
