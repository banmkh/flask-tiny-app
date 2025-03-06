import sqlite3
from faker import Faker
import random

def create_fake_data(db_name="blog.db", num_users=10, num_posts=200):
    fake = Faker()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Generate fake users
    users = []
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = "1234"
        is_admin = 0
        is_ban = 0
        cursor.execute("INSERT INTO users (username, email, password, is_admin, is_ban) VALUES (?, ?, ?, ?, ?)",
                       (username, email, password, is_admin, is_ban))
        users.append(username)
    
    # Generate fake posts
    for _ in range(num_posts):
        title = fake.sentence()
        content = fake.paragraph(nb_sentences=5)
        username = random.choice(users)  # Assign random user to post
        cursor.execute("INSERT INTO posts (title, content, username) VALUES (?, ?, ?)",
                       (title, content, username))
    
    conn.commit()
    conn.close()
    print(f"Generated {num_users} users and {num_posts} posts successfully!")

if __name__ == "__main__":
    create_fake_data()
