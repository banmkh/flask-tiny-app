from flask import Blueprint, render_template,request,redirect,url_for,flash
from flask_login import login_user, logout_user, UserMixin,current_user,login_required
from app.db import get_db, add_user, get_user_by_email, get_user_by_username,get_user_by_id, add_post, get_post_by_id
from app.routes_account import User
post_bp = Blueprint("post_bp", __name__)

# trang chủ
@post_bp.route("/")
def home():

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 2, type=int)

    db = get_db()
    total_posts = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    total_pages = (total_posts + per_page - 1) // per_page 
    posts = db.execute(
        "SELECT * FROM posts ORDER BY date_posted"
    ).fetchall()
    return render_template("index.html", posts=posts,per_page = per_page,page = page,total_pages=total_pages,current_user = current_user)

# thêm 1 bài viết mới
@post_bp.route("/add_new_post",methods = ["GET","POST"])
@login_required
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if not title or not content:
            flash("Tiêu đề và nội dung không được để trống!", "danger")
        else:
            add_post(title, content, current_user.username)
            flash("Bài viết đã được thêm thành công!", "success")
            return redirect(url_for("post_bp.home"))
    return render_template("new_post.html", current_user=current_user)

# xem thông tin của bài viết 
@post_bp.route("/post/<int:post_id>")
def post_detail(post_id):
    post = get_post_by_id(post_id)
    if not post:
        flash("Bài viết không tồn tại!", "danger")
        return redirect(url_for("post_bp.home"))

    return render_template("post_detail.html", post=post)

# Viết thêm chức năng xoá bài viết
@post_bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id = ? AND username = ?", (post_id, current_user.username)).fetchone()
    
    if not post:
        flash("Bài viết không tồn tại hoặc bạn không có quyền xóa!", "danger")
        return redirect(url_for("post_bp.home"))
    
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    
    flash("Bài viết đã được xóa thành công!", "success")
    return redirect(url_for("post_bp.home"))

# Viết chức năng chỉnh sửa bài viết
@post_bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id = ? AND username = ?", (post_id, current_user.username)).fetchone()
    
    if not post:
        flash("Bài viết không tồn tại hoặc bạn không có quyền chỉnh sửa!", "danger")
        return redirect(url_for("post_bp.home"))
    
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if not title or not content:
            flash("Tiêu đề và nội dung không được để trống!", "danger")
        else:
            db.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?",(title, content, post_id))
            db.commit()
            flash("Bài viết đã được cập nhật", "success")
            return redirect(url_for("post_bp.post_detail", post_id=post_id))
            
    return render_template("edit_post.html", post=post, current_user=current_user)

