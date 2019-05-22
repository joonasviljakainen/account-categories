from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from wtforms.fields.html5 import DecimalField, DateField
from re import RegexFlag

class TransactionForm(FlaskForm):
    #amount = DecimalField("Transaction amount", [
    #    validators.Required(True), 
    #    validators.NumberRange(min=0, max=100000000, message="Amount must be over 0.00!") ], 
    #    places=2)
    #amount = DecimalField("Transaction amount", validators=[validators.NumberRange(min=1, max=4)], places=4)
    amount = DecimalField('Transaction amount (with two decimals, e.g. "34.56")', places=3, validators=[validators.NumberRange(min=0, max=100000000)], default=0.00 )
    bookingdate = DateField("Booking date", format="dd/mm/YYYY")
    counterparty = StringField("Name of counterparty", [validators.InputRequired(True)]) 
    iban = StringField("IBAN of counterparty", [
        validators.Required(True), 
        validators.Regexp(r"[A-Z]{2,2}[0-9]{12,20}", message="Invalid IBAN!")]) # Basic validation
    message = StringField("Message or reference number", [validators.Required(True), validators.Length(max=150)])
    creditordebit = SelectField("Payment to you or by you?", choices=[("CREDIT", "To me"), ("DEBIT", "By me")])


    class Meta:
        csrf = False