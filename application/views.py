from flask import render_template
from application import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks")
def get_tasks():
    return "task view not implemented yet"

@app.route("/tasks/new")
def form_task():
    return "HULLO DOG"

@app.route("/transactions/", methods=["POST"])
def create_task():
    print(request.form.get("amount"))
    return "HELLA COOL"
