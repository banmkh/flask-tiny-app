from flask import Blueprint, render_template
from app.db import get_db

main = Blueprint("main", __name__)

@main.route("/")
def home():
    db = get_db()
    posts = db.execute("SELECT * FROM posts").fetchall()
    return render_template("index.html", posts=posts)
