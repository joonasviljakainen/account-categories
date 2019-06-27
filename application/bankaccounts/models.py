from application import db
from application.models import Base
from sqlalchemy.sql import text

class BankAccount(Base):
    __tablename__ = "bankaccount"

    bank = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(144), default="Checking account")

    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    transactions = db.relationship("Transaction", backref="transactions", lazy = True)
    initial_balance = db.Column(db.Numeric, default=0.00)
    current_balance = db.Column(db.Numeric, default=0.00)

    @staticmethod
    def get_number_of_transactions_on_account(bankaccount_id):
        stmt = text("SELECT COUNT(*) FROM transact"
                    " WHERE transact.bankaccount_id = :bankaccount_id").params(bankaccount_id=bankaccount_id)

        res = db.engine.execute(stmt)
        response = []
        for r in res:
            response.append({
                "count" : r[0]
            })
        return response[0].get("count")

    @staticmethod
    def get_transactions_and_categories(bankaccount_id, sortOrder, pageNumber, pageSize):
        stmt = text("SELECT * FROM transact"
                    " LEFT JOIN Category ON transact.category_id = Category.id"
                    " WHERE transact.bankaccount_id = :bankaccount_id"
                    " ORDER BY transact.booking_date DESC"
                    " LIMIT :pageSize OFFSET :pageNumber").params(bankaccount_id=bankaccount_id, sortOrder=sortOrder, pageSize=pageSize, pageNumber=int(pageNumber) * int(pageSize))

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

        return response
