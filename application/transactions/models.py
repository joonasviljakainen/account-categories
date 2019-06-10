from application import db
from application.models import Base
from sqlalchemy.sql import text

class Transaction(Base):
    __tablename__ = "transact"

    booking_date = db.Column(db.Date, default=db.func.current_timestamp())
    value_date = db.Column(db.Date, default=db.func.current_timestamp())
    bankaccount_id = db.Column(db.Integer, db.ForeignKey('bankaccount.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    counterparty_name = db.Column(db.String(144), nullable=False)
    amount = db.Column(db.Numeric(), nullable=False)

    # Type: card, transfer, salary...
    transaction_type = db.Column(db.String(30), nullable=False)
    message = db.Column(db.String(250), nullable=True)
    credit_or_debit = db.Column(db.String(6), nullable=False)

    @staticmethod
    def get_transaction_and_category(transaction_id):
        stmt = text("SELECT * FROM transact"
                    " LEFT JOIN Category ON transact.category_id = Category.id"
                    " WHERE transact.id = :transaction_id").params(transaction_id=transaction_id)

        res = db.engine.execute(stmt)
        response = []
        for r in res:

            response.append({
            "id" : r[0],
            "created_at" : r[1],
            "modified_at" : r[2],
            "booking_date" : r[3],
            "value_date" : r[4],
            "bankaccount_id" : r[5],
            "category_id" : r[6],
            "counterparty_name" : r[7],
            "amount" : r[8],
            "transaction_type" : r[9],
            "message":  r[10],
            "credit_or_debit" : r[11],
            "category_name" : r[13]
        })

        return response[0]

