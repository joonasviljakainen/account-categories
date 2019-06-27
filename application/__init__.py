from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)


# SQLALCHEMY
from flask_sqlalchemy import SQLAlchemy

import os

# set up transaction db
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///transactions.db"
    # request constant logging & debug
    app.config["SQLALCHEMY_ECHO"] = True

# Create database object
db = SQLAlchemy(app)


# Login
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "You need to log in to do that."

# roles in login_required
from functools import wraps

def login_required(roles=["ANY"]):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()
          
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            unauthorized = False

            if roles != ["ANY"]:
                unauthorized = True
                user_role = current_user.get_role()                    
                print(user_role)
                for role in roles:
                    print(role)
                    if current_user.get_role() == role:
                        unauthorized = False
                        break

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


from application.auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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

# Creating all database tables
try:
    db.create_all()
except:
    pass
