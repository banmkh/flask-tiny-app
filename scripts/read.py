import sqlite3

conn = sqlite3.connect("blog.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM posts")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()