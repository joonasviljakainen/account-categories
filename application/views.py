from flask import render_template, request, redirect, url_for
from flask_login import current_user
from application import app, db, login_required
from application.transactions.models import Transaction
from application.transactions.forms import TransactionForm
from application.categories.forms import CategoryUpdateForm
from application.categories.models import Category
from decimal import Decimal
import datetime

from application.bankaccounts.models import BankAccount


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/transactions")
@login_required(roles=["USER","ADMIN"])
def get_transactions():
    categoryForm = CategoryUpdateForm()
    ts = Transaction.query.filter(Transaction.bankaccount_id.in_(map(lambda bankaccount: bankaccount.id, current_user.bankaccounts)))
    return render_template("transactionlist.html", transactions = ts, form = categoryForm)


@app.route("/transactions/<transaction_id>/", methods=["GET"])
@login_required(roles=["USER","ADMIN"])
def get_transaction(transaction_id):
    categoryForm = CategoryUpdateForm()
    t = Transaction.get_transaction_and_category(transaction_id)
    if current_user.id == t.get("owner_id"):
        return render_template("transaction.html", transaction = t, form = categoryForm)
    else:
        return redirect(url_for('auth_login'))


@app.route("/transactions/<transaction_id>/deletions", methods=["POST"])
@login_required(roles=["USER", "ADMIN"])
def delete_transaction(transaction_id):

    t = Transaction.query.filter_by(id=transaction_id).first()
    if t and t.bankaccount_id in (map(lambda x: x.id, current_user.bankaccounts)):
        # transaction owned by current user
        remove_transaction_amount_from_account(t)
        db.session.delete(t)
        db.session.commit()
        return redirect(url_for('bankaccounts'))
    else:
        return "Unauthorized, fool!"


@app.route("/transactions/<transaction_id>", methods=["POST"])
@login_required(roles=["USER","ADMIN"])
def modify_transaction(transaction_id):

    t = Transaction.query.get(transaction_id)
    if t and t.bankaccount_id in (map(lambda x: x.id, current_user.bankaccounts)):
        t.message = request.form.get("message")
        db.session().commit()
        return redirect(url_for("get_transaction", transaction_id=t.id))
    else:
        return redirect(url_for('auth_login'))


@app.route("/transactions/<transaction_id>/categories", methods=["POST"])
@login_required(roles=["USER","ADMIN"])
def set_transaction_category(transaction_id):
    f = CategoryUpdateForm(request.form)
    if f.account.data == 0:
        # TODO: alternate route for returning to the view of a single transaction
        # Return redirect to the transaction
        return "Not implemented yet"
    else: 
        if f.account.data == "---" or f.account.data == "":
            return redirect( url_for("get_bankaccount", bankaccount_id=f.account.data) )

        t = Transaction.query.filter_by(id=transaction_id).first()
        cat = Category.query.filter_by(id=f.category.data).first()

        if t and t.bankaccount_id in (map(lambda x: x.id, current_user.bankaccounts)) and cat:
            t.category_id = f.category.data
            db.session().commit()

            return redirect( url_for("get_bankaccount", bankaccount_id=f.account.data) )
        else:
            return "Unauthorized"


@app.route("/transactions/new")
@login_required(roles=["USER","ADMIN"])
def transaction_form():

    form = TransactionForm()
    accs = current_user.bankaccounts
    cats = current_user.categories
    
    form.account.choices = [(acc.id, acc.name) for acc in accs]
    form.category.choices = [(cat.id, cat.name) for cat in cats]
    return render_template("newtransaction.html", form = form)


@app.route("/transactions", methods=["POST"])
@login_required(roles=["USER","ADMIN"])
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
        # Account not owned by userprint
        # TODO inform user of this
        return redirect("/")

    #AUTHORiZED

    t.bankaccount_id = requestedAccount

    t.amount = Decimal(request.form.get("amount"))
    t.message = request.form.get("message")
    t.credit_or_debit = request.form.get("creditordebit")
    t.counterparty_name = request.form.get("counterparty")
    t.category_id = request.form.get("category")

    booking_date = datetime.datetime.strptime(request.form.get("bookingdate"), "%Y-%m-%d")
    t.booking_date = booking_date

    db.session().add(t)
    db.session().commit()

    add_transaction_amount_to_account(t)

    # Redirect to view with new transaction
    return redirect(url_for("get_transaction", transaction_id=t.id))

# adds transaction amount to account balance if transaction datetime is at
# or after the creation date of the account
def add_transaction_amount_to_account(t):
    account = BankAccount.query.get(t.bankaccount_id)
    
    if account.date_created.date() <= t.booking_date:
        if t.credit_or_debit == "DEBIT":
            account.current_balance = account.current_balance - t.amount
        if t.credit_or_debit == "CREDIT":
            account.current_balance = account.current_balance + t.amount
        db.session().commit()    
    else:
        return

def remove_transaction_amount_from_account(t):
    account = BankAccount.query.get(t.bankaccount_id)
    if account and account.date_created.date() <= t.booking_date:
        if t.credit_or_debit == "DEBIT":
            account.current_balance = account.current_balance + t.amount
        if t.credit_or_debit == "CREDIT":
            account.current_balance = account.current_balance - t.amount
        db.session().commit()   
    else:
        return 

# MONETARY FORMATTING: string
def format_number_string(numberString): # TODO move to another module
    split = numberString.split(".")

    if len(split) == 1 :
        return (numberString + ".00")
    if len(split[1]) < 2:
        numberString = "" + numberString + "0"
    return numberString  