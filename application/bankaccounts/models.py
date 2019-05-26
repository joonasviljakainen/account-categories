from application import db

class BankAccount(db.Model):
    __tablename__ = "bankaccount"

    id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(144), default="Checking account")

    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    transactions = db.relationship("Transaction", backref="transaction", lazy = True)

    # EURO CENTS pls
    balance = db.Column(db.Integer, default=0)