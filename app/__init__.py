from flask import Flask
from app.db import get_db, close_db,get_user_by_id
from flask_login import LoginManager
from app.routes import User

# login_manager = LoginManager()
def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev"

    # đóng database khi request kêt thúc
    app.teardown_appcontext(close_db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    # cấu hình login
    @login_manager.user_loader
    def load_user(user_id):
        user =  get_user_by_id(user_id)
        return User(user['id'],user['username'],user['email'],user['is_admin'])

    from app.routes import main
    app.register_blueprint(main)
    return app
