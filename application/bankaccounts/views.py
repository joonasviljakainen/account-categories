from flask import render_template, request, redirect, url_for

from application import app, db
from application.bankaccounts.models import BankAccount
from application.bankaccounts.forms import AccountForm

@app.route("/bankaccounts", methods = ["GET", "POST"])
def bankaccounts():
    if request.method == "GET":
        return render_template("/bankaccounts/bankaccounts.html", accounts = BankAccount.query.all() , form = AccountForm())

    form = AccountForm(request.form)
    ## TODO validations

    #TODO: Check whether something like this exists 
    #  account = BankAccount.query.filter_by()

    
    print("Creating bank account with name " + form.name.data)
    a = BankAccount()
    a.name = form.name.data
    a.bank = form.bank.data
    if a.balance:
        a.balance = form.balance.data

    db.session().add(a)
    db.session().commit()

    return redirect(url_for("bankaccounts"))
    
