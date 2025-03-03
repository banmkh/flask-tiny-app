from flask import Blueprint, render_template,request,redirect,url_for,flash
from flask_login import login_user, logout_user, UserMixin,current_user,login_required
from app.db import get_db, add_user, get_user_by_email, get_user_by_username,get_user_by_id, add_post, get_post_by_id

main = Blueprint("main", __name__)

class User(UserMixin):
    def __init__(self, id, username, email,is_admin,is_ban):
        self.id = id
        self.username = username
        self.email = email
        self.is_admin = is_admin
        self.is_ban = is_ban

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
    if current_user.is_authenticated:
        flash("Bạn đã đăng nhập rồi!", "info")
        return redirect(url_for("main.home"))
    
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if get_user_by_email(email):
            flash('email đã tồn tại!',"danger")
            redirect(url_for("register.html"))
        elif get_user_by_username(username):
            flash('username đã tồn tại!',"danger")
            redirect(url_for("register.html"))
        else:
            flash("Đăng ký thành công!", "success")
            add_user(username,email,password)
            return redirect(url_for("main.login"))
    return render_template("register.html",current_user = current_user)

# route tới trang login
@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Bạn đã đăng nhập rồi!", "info")
        return redirect(url_for("main.home"))
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = get_user_by_email(email)
        if user and user["password"] == password:
            if user["is_ban"] == 1:
                return redirect(url_for("main.ban"))
            login_user(User(user['id'],user["username"], user["email"],user["is_admin"],user["is_ban"]))
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Email hoặc mật khẩu không đúng!", "danger")
    return render_template("login.html",current_user = current_user)
# logout
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
            add_post(title, content, current_user.username)
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

@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/contact")
def contact():
    return render_template("contact.html")

# thêm chức năng quản lý user của admin
@main.route("/admin/users",methods = ["POST","GET"])
@login_required
def admin_users():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash("Bạn không có quyền truy cập!", "danger")
        return redirect(url_for("main.home"))
    db = get_db()
    users_is_not_ban = db.execute("SELECT id, username, email FROM users WHERE is_admin = 0 and is_ban = 0").fetchall()
    users_is_ban = db.execute("SELECT id, username, email FROM users WHERE is_admin = 0 and is_ban = 1").fetchall()
    for i in users_is_ban:
        print(dict(i))
    return render_template("admin_users.html", users_is_not_ban = users_is_not_ban,users_is_ban = users_is_ban)

# Viết thêm chức năng xoá bài viết
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

# Viết chức năng chỉnh sửa bài viết
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

# Chức năng thông báo khi tài khoản bị cấm
@main.route("/ban")
def ban(is_ban = 0):
    if is_ban == 1:
        return render_template("ban.html")
    else:
        flash("Tài khoản của bạn không thuộc diện bị cấm","danger")
        return redirect(url_for("main.home"))

@main.route("/admin/toggle-ban",methods = ["POST"])
@login_required
def toggle_ban():
    if not current_user.is_admin:
        flash("Bạn không có quyền thực hiện thao tác này!", "danger")
        return redirect(url_for("main.admin_users"))

    selecteds = request.form.getlist("ban_user")
    print(selecteds)
    for id in selecteds:
        db = get_db()
        db.execute("UPDATE users SET is_ban = 1 WHERE id = ?", (id,))
    selecteds = request.form.getlist("un_ban_user")
    for id in selecteds:
        db = get_db()
        db.execute("UPDATE users SET is_ban = 0 WHERE id = ?", (id,))
    db.commit()
    flash("Cập nhật trạng thái thành công!", "success")
    return redirect(url_for("main.admin_users"))