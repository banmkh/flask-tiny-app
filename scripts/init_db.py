import sqlite3

DATABASE = "blog.db"

TABLES = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """,
    "posts": """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """,
    "comments": """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
        );
    """
}

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    for table, query in TABLES.items():
        cursor.execute(query)
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
