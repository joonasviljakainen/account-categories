from application import db

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(144), default="Checking account")

    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    
    # TODO:  Owner

    # EURO CENTS pls
    balance = db.Column(db.Integer, default=0)