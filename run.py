from flask import Flask, render_template
from application import app
import os

if __name__ == "__main__":
    #app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    if (os.environ.get("HEROKU") == 1):
        print("RUNNING IN PRODUCTION MODE")
        app.run(host="0.0.0.0")    
    else:
        print("RUNNING IN DEBUG MODE")
        app.run(debug=True)
    #app.run(host="0.0.0.0")
