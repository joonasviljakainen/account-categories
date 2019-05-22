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

# Creating all database tables
db.create_all()
