from flask import Flask
from app.db import get_db, close_db

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "your_secret_key"
    app.teardown_appcontext(close_db)
    from app.routes import main
    app.register_blueprint(main)
    return app
