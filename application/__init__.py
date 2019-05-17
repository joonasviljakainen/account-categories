from flask import Flask
app = Flask(__name__)

# SQLALCHEMY
from flask_sqlalchemy import SQLAlchemy

# set up transaction db
app.conficg["SQLALCHEMY_DATABASE_URI] = "sqlite:///tseks.db"

# request constant logging & debug
app.config["SQLALCHEMY_ECHO"] = True

# Create database object
db = SQLAlchemy(app)

from application import views

# Creating all database tables

db.create_all()
