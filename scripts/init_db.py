import sqlite3

DATABASE = "blog.db"

TABLES = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            is_ban INTEGER DEFAULT 0
        );
    """,
    "is_admin_feature": """
        ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0;
    """,
    "is_ban_feature":"""
        ALTER TABLE users ADD COLUMN is_ban INTEGER DEFAULT 0;
    """,
    "author_feature":"""
        ALTER TABLE posts ADD COLUMN username TEXT;
    """,
    "posts": """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            username TEXT,
            date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    for table_or_feature_name, query in TABLES.items():
        try:
            cursor.execute(query)
        except:
            print(f"{table_or_feature_name} đã tồn tại!!!")
    
    conn.commit()
    if conn.execute("SELECT count(*) FROM users WHERE is_admin == 1").fetchall() == 0:
        conn.execute(
            "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
            ("admin", "admin@example.com", "1234", 1))
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
