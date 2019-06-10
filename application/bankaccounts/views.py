from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from pprint import pprint
from decimal import Decimal

from application import app, db
from application.bankaccounts.models import BankAccount
from application.bankaccounts.forms import AccountForm
from application.categories.forms import CategoryUpdateForm
from application.transactions.models import Transaction

@app.route("/bankaccounts/<bankaccount_id>")
@login_required
def get_bankaccount(bankaccount_id):
    transactions = BankAccount.get_transactions_and_categories(bankaccount_id)
    bankaccount = BankAccount.query.filter_by(id=bankaccount_id).first()
    if current_user.id == bankaccount.user_id:
        cats = current_user.categories
        categoryForm = CategoryUpdateForm(request.values, account=bankaccount_id)
        categoryForm.category.choices = [("", "---")]+[(cat.id, cat.name) for cat in cats]
        return render_template("/bankaccounts/singlebankaccount.html", account = bankaccount, transactions = transactions, form = categoryForm)

@app.route("/bankaccounts/<bankaccount_id>/summary")
@login_required
def get_bankaccount_summary(bankaccount_id):

    bankaccount = BankAccount.query.filter_by(id=bankaccount_id).first()
    if bankaccount.user_id != current_user.id:
        return "Unauthorized"

    summarydata = Transaction.get_sum_of_debit_transactions_by_category(bankaccount_id)
    print(summarydata)
    return render_template("/bankaccounts/accountsummary.html", account=bankaccount, summary=summarydata)


@app.route("/bankaccounts/<bankaccount_id>/deletion", methods = ["POST"])
@login_required
def delete_bankaccount(bankaccount_id):
    u = current_user
    acc = BankAccount.query.filter_by(id=bankaccount_id).first()

    if u.id == acc.user_id:
        db.session.delete(acc)
        db.session.commit()

        return redirect(url_for("bankaccounts"))

    return "not found"

@app.route("/bankaccounts/<bankaccount_id>/names", methods=["POST"])
def update_bankaccount(bankaccount_id):
    u = current_user
    a = BankAccount.query.get(bankaccount_id)

    if a.user_id == u.id:
        a.name = request.form.get("accountname")
        db.session().commit()
        return redirect(url_for("get_bankaccount", bankaccount_id=bankaccount_id))
    
    return "ERROR"

@app.route("/bankaccounts", methods = ["GET", "POST"])
@login_required
def bankaccounts():
    if request.method == "GET":
        accs = BankAccount.query.filter_by(user_id=current_user.id)
        return render_template("/bankaccounts/bankaccounts.html", accounts = accs , form = AccountForm())

    form = AccountForm(request.form)
    ## TODO validations
    
    a = BankAccount()
    a.user_id = current_user.id
    a.name = form.name.data
    a.bank = form.bank.data
    a.initial_balance = Decimal(form.balance.data)
    a.current_balance = a.initial_balance

    db.session().add(a)
    db.session().commit()

    return redirect(url_for("bankaccounts"))
    
