from application import db

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    #transactions = db.relationship("Transaction", backref="transaction", lazy = True)

    # TODO: Add connection to counterparties