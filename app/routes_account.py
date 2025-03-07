from flask import Blueprint, render_template,request,redirect,url_for,flash
from flask_login import login_user, logout_user, UserMixin,current_user,login_required
from app.db import get_db, add_user, get_user_by_email, get_user_by_username,get_user_by_id, add_post, get_post_by_id

user_bp  = Blueprint("user_bp", __name__)

class User(UserMixin):
    def __init__(self, id, username, email,is_admin,is_ban):
        self.id = id
        self.username = username
        self.email = email
        self.is_admin = is_admin
        self.is_ban = is_ban

    def get_id(self):
        return str(self.id)


# route tới trang đăng ký
@user_bp.route("/register",methods = ["GET","POST"])
def register():
    if current_user.is_authenticated:
        flash("Bạn đã đăng nhập rồi!", "info")
        return redirect(url_for("post_bp.home"))
    
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if get_user_by_email(email):
            flash('email đã tồn tại!',"danger")
            return redirect(url_for("user_bp.register"))  # Fixed endpoint
        elif get_user_by_username(username):
            flash('username đã tồn tại!',"danger")
            return redirect(url_for("user_bp.register"))  # Fixed endpoint
        else:
            flash("Đăng ký thành công!", "success")
            add_user(username,email,password)
            return redirect(url_for("user_bp.login"))
    return render_template("register.html",current_user = current_user)

# route tới trang login
@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Bạn đã đăng nhập rồi!", "info")
        return redirect(url_for("post_bp.home"))
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = get_user_by_email(email)
        if user and user["password"] == password:
            if user["is_ban"] == 1:
                flash("tài khoản của bạn đã bị cấm, vui lòng liên hệ admin để bỏ cấm",'danger')
                return redirect(url_for("user_bp.contact",is_ban = 1))
            login_user(User(user['id'],user["username"], user["email"],user["is_admin"],user["is_ban"]))
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("post_bp.home"))
        else:
            flash("Email hoặc mật khẩu không đúng!", "danger")
    return render_template("login.html",current_user = current_user)
# logout
@user_bp.route("/logout")
def logout():
    logout_user()
    flash("Đã đăng xuất!", "info")
    return redirect(url_for("post_bp.home"))

@user_bp.route("/about")
def about():
    return render_template("about.html")

@user_bp.route("/contact")
def contact():
    return render_template("contact.html")

# thêm chức năng quản lý user của admin
@user_bp.route("/admin/users", methods=["POST", "GET"])
@login_required
def admin_users():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash("Bạn không có quyền truy cập!", "danger")
        return redirect(url_for("post_bp.home"))
    db = get_db()
    users_is_not_ban = db.execute("SELECT id, username, email FROM users WHERE is_admin = 0 and is_ban = 0").fetchall()
    users_is_ban = db.execute("SELECT id, username, email FROM users WHERE is_admin = 0 and is_ban = 1").fetchall()
    return render_template("admin_users.html", users_is_not_ban=users_is_not_ban, users_is_ban=users_is_ban)

# Chức năng cấm, bỏ cấm tài khoản - đã có sẵn
@user_bp.route("/admin/toggle-ban", methods=["POST"])
@login_required
def toggle_ban():
    if not current_user.is_admin:
        flash("Bạn không có quyền thực hiện thao tác này!", "danger")
        return redirect(url_for("user_bp.admin_users"))

    # Lấy kết nối database trước khi thực hiện các thao tác
    db = get_db()
    
    selecteds = request.form.getlist("ban_user")
    print(selecteds)
    for id in selecteds:
        db.execute("UPDATE users SET is_ban = 1 WHERE id = ?", (id,))
        
    selecteds = request.form.getlist("un_ban_user")
    for id in selecteds:
        db.execute("UPDATE users SET is_ban = 0 WHERE id = ?", (id,))
        
    db.commit()
    flash("Cập nhật trạng thái thành công!", "success")
    return redirect(url_for("user_bp.admin_users"))

# Chức năng đổi mật khẩu
@user_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        user = get_user_by_id(current_user.id)
        if not user or user["password"] != old_password:
            flash("Mật khẩu cũ không chính xác!", "danger")
            return redirect(url_for("user_bp.change_password"))
        
        if new_password != confirm_password:
            flash("Mật khẩu mới và xác nhận mật khẩu không khớp!", "danger")
            return redirect(url_for("user_bp.change_password"))
        
        db = get_db()
        db.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, current_user.id))
        db.commit()
        
        flash("Đổi mật khẩu thành công!", "success")
        return redirect(url_for("post_bp.home"))
    
    return render_template("change_password.html", current_user=current_user)

# reset pass cho user
@user_bp.route("/admin/reset-password/<int:user_id>", methods=["GET", "POST"])
@login_required
def reset_password(user_id):
    if not current_user.is_authenticated or not current_user.is_admin:
        flash("Bạn không có quyền thực hiện thao tác này!", "danger")
        return redirect(url_for("post_bp.home"))
    
    user = get_user_by_id(user_id)
    if not user:
        flash("Không tìm thấy người dùng!", "danger")
        return redirect(url_for("user_bp.admin_users"))
    
    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        
        if new_password != confirm_password:
            flash("Mật khẩu mới và xác nhận mật khẩu không khớp!", "danger")
            return redirect(url_for("user_bp.reset_password", user_id=user_id))
        
        db = get_db()
        db.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
        db.commit()
        flash(f"Đã đặt lại mật khẩu cho người dùng {user['username']}!", "success")
        return redirect(url_for("user_bp.admin_users"))
    
    return render_template("admin_reset_password.html", user=user)

# xem tri tiết người dùng
@user_bp.route("/admin/user-detail/<int:user_id>")
@login_required
def user_detail(user_id):
    if not current_user.is_authenticated or not current_user.is_admin:
        flash("Bạn không có quyền thực hiện thao tác này!", "danger")
        return redirect(url_for("post_bp.home"))
    
    user = get_user_by_id(user_id)
    if not user:
        flash("Không tìm thấy người dùng!", "danger")
        return redirect(url_for("user_bp.admin_users"))
    
    db = get_db()
    posts = db.execute("SELECT * FROM posts WHERE username = ? ORDER BY date_posted DESC", (user['username'],)).fetchall()
    
    return render_template("admin_user_detail.html", user=user, posts=posts)
