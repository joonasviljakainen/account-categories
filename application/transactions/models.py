from application import db

class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.Date, default=db.func.current_timestamp())
    value_date = db.Column(db.Date, default=db.func.current_timestamp())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    #user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    bankaccount_id = db.Column(db.Integer, db.ForeignKey('bankaccount.id'), nullable=False)

    counterparty_name = db.Column(db.String(144), nullable=False)
    amount = db.Column(db.String(10), nullable=False)

    # Type: card, transfer, salary...
    transaction_type = db.Column(db.String(30), nullable=False)
    message = db.Column(db.String(250), nullable=True)
    credit_or_debit = db.Column(db.String(6), nullable=False)
