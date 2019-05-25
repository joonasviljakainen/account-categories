from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class AccountForm(FlaskForm):
    
    name = StringField("Name", validators=[validators.Length(min=1, max=40)])
    bank = StringField("Name of bank", validators=[validators.InputRequired(True), validators.Length(min=1, max=40)])
    balance = IntegerField("Current balance (in euro cents", validators=[validators.NumberRange(min=-10000000, max = 10000000)])
