import sqlite3

conn = sqlite3.connect("blog.db")
cursor = conn.cursor()
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()