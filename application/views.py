from flask import render_template, request
from application import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transactions")
def get_transactions():
    return "transaction view not implemented yet"

@app.route("/transactions/new")
def transaction_form():
    return render_template("newtransaction.html")

@app.route("/transactions", methods=["POST"])
def create_transaction():
    print(request.form.get("name"))
    return "HELLA COOL"
