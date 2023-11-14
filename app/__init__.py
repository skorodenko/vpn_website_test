import os
import logging
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

USER = os.environ["POSTGRES_USER"]
PASSWORD = os.environ["POSTGRES_PASSWORD"]
HOST = os.environ["POSTGRES_HOST"]
PORT = os.environ["POSTGRES_PORT"]
DB = os.environ["POSTGRES_DB"]

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
logger = logging.getLogger("app.manual")

def create_app():
    app = Flask(__name__)
    app.config.from_mapping({
        "SECRET_KEY": os.urandom(64),
        "SQLALCHEMY_DATABASE_URI": f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DB}",
    })
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = "auth.login"

    from .views import bp_root
    app.register_blueprint(bp_root)
    
    with app.app_context():
        db.create_all()
    
    return app