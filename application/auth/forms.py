from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False

class CreateUserForm(FlaskForm):
    displayname = StringField("Display name (What we'll call you")
    username = StringField("Usename (your user ID)")
    password = PasswordField("Password", validators=[validators.EqualTo('pwdvalidation')])
    pwdvalidation = PasswordField("Repeat password")

    class Meta:
        scrf = False
    