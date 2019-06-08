from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application import app, db
from application.transactions.models import Transaction
from application.transactions.forms import TransactionForm
from decimal import Decimal

from application.bankaccounts.models import BankAccount


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/transactions")
@login_required
def get_transactions():
    ts = Transaction.query.filter(Transaction.bankaccount_id.in_(map(lambda bankaccount: bankaccount.id, current_user.bankaccounts)))
    return render_template("transactionlist.html", transactions = ts)


@app.route("/transactions/<transaction_id>/", methods=["GET"])
@login_required
def get_transaction(transaction_id):
    t = Transaction.get_transaction_and_category(transaction_id)
    return render_template("transaction.html", transaction = t)
    #return render_template("transaction.html", transaction = Transaction.query.get(transaction_id))


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

    form = TransactionForm()
    accs = current_user.bankaccounts
    cats = current_user.categories
    
    form.account.choices = [(acc.id, acc.name) for acc in accs]
    form.category.choices = [(cat.id, cat.name) for cat in cats]
    return render_template("newtransaction.html", form = form)

# MONETARY FORMATTING: string
def format_number_string(numberString): # TODO move to another module
    split = numberString.split(".")

    if len(split) == 1 :
        return (numberString + ".00")
    if len(split[1]) < 2:
        numberString = "" + numberString + "0"
    return numberString


@app.route("/transactions", methods=["POST"])
@login_required
def create_transaction():
    t = Transaction()
    t.transaction_type = "TRANSFER" # Preset pending value determination
    
    # OWNERSHIP VALIDATION
    isOwn = False
    requestedAccount = int(request.form.get("account"))
    for g in current_user.bankaccounts:
        if g.id == requestedAccount:
            isOwn = True
            break
    
    if isOwn == False:
        # Account not owned by userprint("Wrong move, buster")
        # TODO inform user of this
        return redirect("/")

    #AUTHOROZED

    t.bankaccount_id = requestedAccount

    t.amount = Decimal(request.form.get("amount"))
    t.message = request.form.get("message")
    t.credit_or_debit = request.form.get("creditordebit")
    t.counterparty_name = request.form.get("counterparty")
    t.category_id = request.form.get("category")

    db.session().add(t)
    db.session().commit()

    # ADDING TRANSACTION SUM TO ACCOUNT BALANCE
    add_transaction_amount_to_account(t)

    # Redirect to view with new transaction
    return redirect(url_for("get_transaction", transaction_id=t.id))
    #return redirect(url_for("get_transactions"))

def add_transaction_amount_to_account(t):
    account = BankAccount.query.get(t.bankaccount_id)
    if t.credit_or_debit == "DEBIT":
        account.current_balance = account.current_balance - t.amount
    if t.credit_or_debit == "CREDIT":
        account.current_balance = account.current_balance + t.amount

    db.session().commit()      