import sqlite3

conn = sqlite3.connect("database/support_system.db")

print("Foreign key enforcement:",
      conn.execute("PRAGMA foreign_keys").fetchone()[0])

conn.close()