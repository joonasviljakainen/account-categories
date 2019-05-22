from flask import render_template, request, redirect, url_for
from flask_login import login_required
from application import app, db
from application.transactions.models import Transaction
from application.transactions.forms import TransactionForm


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/transactions")
@login_required
def get_transactions():
    return render_template("transactionlist.html", transactions = Transaction.query.all())

@app.route("/transactions/<transaction_id>/", methods=["GET"])
@login_required
def get_transaction(transaction_id):
    return render_template("transaction.html", transaction = Transaction.query.get(transaction_id))


@app.route("/transactions/<transaction_id>/", methods=["POST"])
@login_required
def modify_transaction(transaction_id):

    t = Transaction.query.get(transaction_id)
    t.message = request.form.get("message")
    db.session().commit()

    return redirect(url_for("get_transaction", transaction_id=t.id))

@app.route("/transactions/new")
@login_required
def transaction_form():
    #return render_template("newtransaction.html")
    return render_template("newtransaction.html", form = TransactionForm())


def format_number_string(numberString): # TODO move to another module
    split = numberString.split(".")

    if len(split) :
        return (numberString + ".00")
    if len(split[1]) < 2:
        numberString = "" + numberString + "0"
    return numberString

@app.route("/transactions", methods=["POST"])
@login_required
def create_transaction():
    
    
    t = Transaction()
    t.transaction_type = "TRANSFER" # Preset pending value determination

    t.amount = format_number_string(request.form.get("amount")) # string
    t.message = request.form.get("message")
    t.credit_or_debit = request.form.get("creditordebit")
    t.counterparty_name = request.form.get("counterparty")

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("get_transactions"))
