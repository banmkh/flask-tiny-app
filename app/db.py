import sqlite3
from flask import g
from flask_login import LoginManager, UserMixin
from datetime import datetime

DATABASE = "blog.db"
# truy vấn vào database
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Trả về dict thay vì tuple
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
# thêm mới 1 user
def add_user(username,email,password):
    db = get_db()
    db.execute("INSERT into users(username,email,password) VALUES (?,?,?)",(username,email,password))
    db.commit()

# kiểm tra xem email đã được sử dụng hay chưa
def get_user_by_email(email):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    # Remove the print statement and directly return the result
    return dict(user) if user else None

# kiểm tra xem tên user đã được sử dụng hay chưa
def get_user_by_username(username):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    return dict(user) if user != None else None

def get_user_by_id(id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
    return dict(user) if user != None else None

# thêm 1 bài viết mới
def add_post(title, content, user_id):
    """Thêm bài viết mới vào database"""
    db = get_db()
    db.execute(
        "INSERT INTO posts (title, content, user_id, date_posted) VALUES (?, ?, ?, ?)",
        (title, content, user_id, datetime.utcnow()),  # ✅ Thêm `date_posted` bằng Python
    )
    db.commit()

def get_post_by_id(id):
    db = get_db()
    post = db.execute("""
        SELECT posts.id, posts.title, posts.content, posts.date_posted, users.username AS author
        FROM posts
        JOIN users ON posts.user_id = users.id
        WHERE posts.id = ?
    """, (id,)).fetchone()
    return post

