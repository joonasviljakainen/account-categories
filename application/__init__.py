from flask import Flask
app = Flask(__name__)

# SQLALCHEMY
from flask_sqlalchemy import SQLAlchemy

# set up transaction db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///transactions.db"
# request constant logging & debug
app.config["SQLALCHEMY_ECHO"] = True

# Create database object
db = SQLAlchemy(app)

from application import views
from application.transactions import models

from application.auth import models
from application.auth import views

# Login
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "You need to log in to do that."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Creating all database tables
db.create_all()
