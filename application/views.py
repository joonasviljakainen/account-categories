from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
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

    form = TransactionForm()
    accs = current_user.bankaccounts

    #for g in current_user.bankaccounts:
    #    print("adsfölkjfdsa " + str(g.id) + " daf " + g.name )
    
    form.account.choices = [(acc.id, acc.name) for acc in accs]
    return render_template("newtransaction.html", form = form)


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
    else:
        # Account owned by user
        print("Authorized")

    # TODO validate that the transaction creator owns the account
    t.bankaccount_id = requestedAccount
    t.amount = format_number_string(request.form.get("amount")) # string
    t.message = request.form.get("message")
    t.credit_or_debit = request.form.get("creditordebit")
    t.counterparty_name = request.form.get("counterparty")

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("get_transactions"))
