from application import db

class BankAccount(db.Model):
    __tablename__ = "bankaccount"

    id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(144), default="Checking account")

    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    transactions = db.relationship("Transaction", backref="transactions", lazy = True)

    # EURO CENTS pls
    initial_balance = db.Column(db.Numeric, default=0.00)
    current_balance = db.Column(db.Numeric, default=0.00)