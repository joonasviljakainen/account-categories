from application import db

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    categoryTransactions = db.relationship("Transaction", backref="transact", lazy = True)

    # TODO: Add connection to counterparties