import sqlite3

conn = sqlite3.connect("blog.db")
cursor = conn.cursor()
cursor.execute("""
SELECT * from users;
""")
schema = cursor.fetchall()
for i in schema:
    print(i)
# rows = cursor.fetchall()

# for row in rows:
#     print(row)

conn.close()