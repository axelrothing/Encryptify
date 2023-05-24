from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "encryptify_password"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)


    from .views import views
    from .crypt import crypt

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(crypt, url_prefix="/")

    from .models import Encryption_Model

    create_database(app)

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created Database!")










