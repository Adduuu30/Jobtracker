import sqlite3

conn = sqlite3.connect("jobtracker.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE jobs ADD COLUMN user_id INTEGER
""")

conn.commit()
conn.close()

print("user_id column added successfully")