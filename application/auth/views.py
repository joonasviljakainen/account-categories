from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db, bcrypt, login_required
from application.auth.models import User
from application.auth.forms import LoginForm, CreateUserForm
from application.categories.models import Category
from application.transactions.models import Transaction

from sqlalchemy import func


# LOGIN FORM AND LOGIN
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("/auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    ## TODO validation

    user = User.query.filter_by(username=form.username.data).first()

    if not user or not bcrypt.check_password_hash(user.password, form.password.data):
        return render_template("/auth/loginform.html", form = form, error = "Incorrect username or password!")

    login_user(user)
    return redirect(url_for("bankaccounts"))

# LOGOUT
@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

# NEW USER
@app.route("/auth/user/new", methods = ["GET", "POST"])
def create_user():
    if request.method == "GET":
        return render_template("/auth/newuser.html", form = CreateUserForm())

    form = CreateUserForm(request.form)
    user = User.query.filter_by(username=form.username.data).first()

    if not user:
        username = form.username.data
        passwordHash = bcrypt.generate_password_hash(form.password.data).decode("utf-8") ## CHANGE TO BE BCRYPTED
        name = form.displayname.data
        
        # New user
        u = User(name, username, passwordHash)
        # THIS IS A HACK
        if u.name == "admin":
            u.role = "ADMIN"
        else:
            u.role = "USER"

        db.session().add(u)
        db.session().commit()

        # Adding default categories
        Category.create_default_categories(u.id)

        return redirect(url_for("auth_login"))

    return render_template("/auth/newuser.html", form = form, error = "Username already in use! Choose another one.")


@app.route("/admin/stats")
@login_required(roles=["ADMIN"])
def get_admin_stats():
    users = User.query.all()
    transactionNumber = db.session().query(func.count(Transaction.id)).scalar()
    return render_template("/auth/adminstats.html", users=users, numberOfTransactions=transactionNumber)
