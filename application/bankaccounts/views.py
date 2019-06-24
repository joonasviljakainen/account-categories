from flask import render_template, request, redirect, url_for, json
from flask_login import current_user##, login_required
from pprint import pprint
from decimal import Decimal
from datetime import datetime

from application import app, db, login_required
from application.bankaccounts.models import BankAccount
from application.bankaccounts.forms import AccountForm
from application.categories.forms import CategoryUpdateForm
from application.transactions.models import Transaction

# Get the info and transactions of a single bank account
@app.route("/bankaccounts/<bankaccount_id>")
@login_required(roles=["USER", "ADMIN"])
def get_bankaccount(bankaccount_id):

    sortOrder = "ASC" if (request.args.get("asc")) else "DESC"
    pageNumber = int(request.args.get("page") if request.args.get("page") else 0)
    pageSize = 3

    bankaccount = BankAccount.query.filter_by(id=bankaccount_id).first()
    if current_user.id == bankaccount.user_id:
        transactions = BankAccount.get_transactions_and_categories(bankaccount_id, sortOrder, pageNumber, pageSize)
        numOfTs = int(BankAccount.get_number_of_transactions_on_account(bankaccount_id))
        eol = pageSize * (pageNumber + 1)

        notLast = True
        if eol >= numOfTs:
            notLast = False

        cats = current_user.categories
        categoryForm = CategoryUpdateForm(request.values, account=bankaccount_id)
        categoryForm.category.choices = [("", "---")]+[(cat.id, cat.name) for cat in cats]
        
        nextPage = int(pageNumber) + 1
        previousPage = int(pageNumber) - 1

        endOfPage = min(numOfTs, pageSize * (pageNumber + 1))

        pagingMessage = ("Showing transactions " + str(pageNumber * pageSize + 1) + " to " + str(endOfPage) + " of " + str(numOfTs))
        if (numOfTs == 0):
            pagingMessage = "No transactions"


        return render_template("/bankaccounts/singlebankaccount.html", 
            account = bankaccount, 
            transactions = transactions, 
            form = categoryForm, 
            currentPage = str(pageNumber), 
            nextPage=nextPage, 
            previousPage=previousPage,
            notLast=notLast,
            pagingMessage = pagingMessage)

# Get a categorized summary of the specified account within a given time frame
@app.route("/bankaccounts/<bankaccount_id>/summary")
@login_required(roles=["USER", "ADMIN"])
def get_bankaccount_summary(bankaccount_id):

    period = request.args.get("period")
    active = period
    now = datetime.now()

    if period == "mtd":
        start_date = datetime(now.year, now.month, 1)
        end_date = now
    elif period == "year":
        start_date = datetime(now.year - 1, now.month, now.day)
        end_date = now
    elif period == "ytd":
        start_date = datetime(now.year, 1, 1)
        end_date = now
    elif period == "all":
        start_date = datetime(1970, 1, 1)
        end_date = now
    elif period == "test":
        start_date = datetime(now.year, now.month, 5)
        end_date = now
    else:
        start_date = datetime(now.year, now.month, 1)
        end_date = now
        active="mtd"

    bankaccount = BankAccount.query.filter_by(id=bankaccount_id).first()
    if bankaccount.user_id != current_user.id:
        return "Unauthorized"

    debitSummaryData = Transaction.get_sum_of_transactions_by_category("DEBIT", bankaccount_id, start_date, end_date)
    debitD = []
    colorList = [ "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA","#ABCDEF", "#DDDDDD", "#ABCABC" ]
    i = 0
    while i < len(debitSummaryData):
        debitD.append({ 'label': debitSummaryData[i].get("name"), 'value': str(debitSummaryData[i].get("amount")), 'color': colorList[i]})
        i = i + 1

    creditSummaryData = Transaction.get_sum_of_transactions_by_category("CREDIT", bankaccount_id, start_date, end_date)
    creditD = []
    i = 0
    while i < len(creditSummaryData):
        creditD.append({ 'label': creditSummaryData[i].get("name"), 'value': str(creditSummaryData[i].get("amount")), 'color': colorList[i]})
        i = i + 1

    return render_template("/bankaccounts/accountsummary.html", 
        account=bankaccount,
        debitSummary=debitSummaryData,
        debitset=debitD,
        creditset=creditD,
        creditSummary=creditSummaryData,
        active=active)


# Delete / Remove bankaccount and related transactions
@app.route("/bankaccounts/<bankaccount_id>/deletion", methods = ["POST"])
@login_required(roles=["USER", "ADMIN"])
def delete_bankaccount(bankaccount_id):
    u = current_user
    acc = BankAccount.query.filter_by(id=bankaccount_id).first()

    if u.id == acc.user_id:
        Transaction.delete_transactions_by_account(acc.id)
        db.session().delete(acc)
        db.session().commit()
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
@login_required(roles=["USER", "ADMIN"])
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
    
