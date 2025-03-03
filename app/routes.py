from flask import Blueprint, render_template,request,redirect,url_for,flash
from flask_login import login_user, logout_user, UserMixin,current_user,login_required
from app.db import get_db, add_user, get_user_by_email, get_user_by_username,get_user_by_id, add_post, get_post_by_id

main = Blueprint("main", __name__)

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    def get_id(self):
        return str(self.id)


@main.route("/")
def home():
    print(current_user.is_authenticated)
    db = get_db()
    posts = db.execute("SELECT * FROM posts").fetchall()
    return render_template("index.html", posts=posts,current_user = current_user)

# route tới trang đăng ký
@main.route("/register",methods = ["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if get_user_by_email(email):
            flash('email đã tồn tại!',"danger")
        elif get_user_by_username(username):
            flash('username đã tồn tại!',"danger")
        else:
            add_user(username,email,password)
            return redirect(url_for("main.login"))
    return render_template("register.html",current_user = current_user)

# route tới trang login
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = get_user_by_email(email)
        if user and user["password"] == password:
            login_user(User(user['id'],user["username"], user["email"]))
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Email hoặc mật khẩu không đúng!", "danger")
    return render_template("login.html",current_user = current_user)
@main.route("/logout")
def logout():
    logout_user()
    flash("Đã đăng xuất!", "info")
    return redirect(url_for("main.home"))

@main.route("/add_new_post",methods = ["GET","POST"])
@login_required
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if not title or not content:
            flash("Tiêu đề và nội dung không được để trống!", "danger")
        else:
            add_post(title, content, current_user.id)  # ✅ Gọi add_post() từ db.py
            flash("Bài viết đã được thêm thành công!", "success")
            return redirect(url_for("main.home"))
    return render_template("new_post.html", current_user=current_user)

@main.route("/post/<int:post_id>")
def post_detail(post_id):
    post = get_post_by_id(post_id)

    if not post:
        flash("Bài viết không tồn tại!", "danger")
        return redirect(url_for("main.home"))

    return render_template("post_detail.html", post=post)

#Viết thêm chức năng xoá bài viết
@main.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id = ? AND user_id = ?", (post_id, current_user.id)).fetchone()
    
    if not post:
        flash("Bài viết không tồn tại hoặc bạn không có quyền xóa!", "danger")
        return redirect(url_for("main.home"))
    
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    
    flash("Bài viết đã được xóa thành công!", "success")
    return redirect(url_for("main.home"))

#Viết chức năng chỉnh sửa bài viết
@main.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id = ? AND user_id = ?", (post_id, current_user.id)).fetchone()
    
    if not post:
        flash("Bài viết không tồn tại hoặc bạn không có quyền chỉnh sửa!", "danger")
        return redirect(url_for("main.home"))
    
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if not title or not content:
            flash("Tiêu đề và nội dung không được để trống!", "danger")
        else:
            db.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?",(title, content, post_id))
            db.commit()
            flash("Bài viết đã được cập nhật", "success")
            return redirect(url_for("main.post_detail", post_id=post_id))
            
    return render_template("edit_post.html", post=post, current_user=current_user)