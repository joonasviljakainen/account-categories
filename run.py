from flask import Flask, render_template
from application import app

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host="0.0.0.0")
