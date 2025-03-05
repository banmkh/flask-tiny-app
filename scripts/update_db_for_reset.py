import sqlite3

def update_database():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if "reset_token" not in columns:
        print("Adding reset_token column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN reset_token TEXT")
    
    if "reset_token_expiry" not in columns:
        print("Adding reset_token_expiry column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN reset_token_expiry TIMESTAMP")
    
    conn.commit()
    conn.close()
    print("Database updated successfully!")

if __name__ == "__main__":
    update_database()