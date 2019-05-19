from flask import render_template, request, redirect, url_for
from application import app, db
from application.transactions.models import Transaction

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/transactions")
def get_transactions():
    return render_template("transactionlist.html", transactions = Transaction.query.all())


@app.route("/transactions/<transaction_id>/", methods=["GET"])
def get_transaction(transaction_id):
    return render_template("transaction.html", transaction = Transaction.query.get(transaction_id))


@app.route("/transactions/<transaction_id>/", methods=["POST"])
def modify_transaction(transaction_id):

    t = Transaction.query.get(transaction_id)
    t.message = request.form.get("message")
    db.session().commit()

    return redirect(url_for("get_transaction", transaction_id=t.id))


@app.route("/transactions/new")
def transaction_form():
    return render_template("newtransaction.html")


@app.route("/transactions", methods=["POST"])
def create_transaction():
    print(request.form.get("name"))
    t = Transaction()
    t.amount = "100.01"
    t.message = request.form.get("name")
    t.credit_or_debit = "DEBIT"
    t.counterparty_name = "SERGEI"
    t.transaction_type = "TRANSFER"

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("get_transactions"))
