from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db, bcrypt
from application.auth.models import User
from application.auth.forms import LoginForm, CreateUserForm
from application.categories.models import Category
#from flask_bcrypt import Bcrypt

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
    return redirect(url_for("index"))

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
        db.session().add(u)
        db.session().commit()

        # Adding default categories
        Category.create_default_categories(u.id)

        return redirect(url_for("index"))

    return render_template("/auth/newuser.html", form = form, error = "Username already in use! Choose another one.")


