from flask import Flask, render_template
from application import app
import os

if __name__ == "__main__":
    heroku = os.environ.get("HEROKU")
    if (heroku == 1 or heroku == "1"):
        print("RUNNING IN PRODUCTION MODE")
        app.run(host="0.0.0.0")    
    else:
        print("RUNNING IN DEBUG MODE")
        app.run(debug=True)
