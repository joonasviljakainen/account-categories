from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, SelectField, validators
from re import RegexFlag

class TransactionForm(FlaskForm):
    amount = DecimalField("Transaction amount", [validators.Required(True), validators.number_range(min=0.00, max=100000000) ])
    bookingdate = DateField("Booking date", format="dd/mm/YYYY")
    counterparty = StringField("Name of counterparty", [validators.InputRequired(True)]) 
    iban = StringField("IBAN of counterparty", [
        validators.Required(True), 
        validators.Regexp("[A-Z]{2,2}[0-9]{12,20}", message="Invalid IBAN!")]) # Basic validation
    message = StringField("Message or reference number")
    creditordebit = SelectField("Payment to you or by you?", choices=[("CREDIT", "To me"), ("DEBIT", "By me")])


    class Meta:
        csrf = False