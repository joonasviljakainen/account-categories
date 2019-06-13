from flask import Flask
import os
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)


# SQLALCHEMY
from flask_sqlalchemy import SQLAlchemy

# set up transaction db
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///transactions.db"
    # request constant logging & debug
    app.config["SQLALCHEMY_ECHO"] = True

# Create database object
db = SQLAlchemy(app)

# Transactions 
from application import views
from application.transactions import models

# Auth
from application.auth import models
from application.auth import views

# Bank accounts
from application.bankaccounts import models
from application.bankaccounts import views

# Categories
from application.categories import models
from application.categories import views

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
try:
    db.create_all()
except:
    pass
