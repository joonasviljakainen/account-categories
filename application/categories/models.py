from application import db
from sqlalchemy.sql import text

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    categoryTransactions = db.relationship("Transaction", backref="transact", lazy = True)

    # TODO: Add connection to counterparties

    @staticmethod
    def create_default_categories(user_id):
        defaultCategories = ["Rent", "Groceries", "Restaurants", "Drinking", "Entertainment", "Commuting", "Travel", "No Category"]

        for cat in defaultCategories:

            c = Category()
            c.user_id = user_id
            c.name = cat
            db.session().add(c)
        
        db.session().commit()
    
    @staticmethod
    def get_transactions_by_account_for_category(category_id):
        #stmt = text("SELECT * FROM category"
        #            " LEFT JOIN transact ON transact.category_id = category.id"
        #            " LEFT JOIN bankaccount ON transact.bankaccount_id = bankaccount_id"
        #            " WHERE category.id = :category_id"
        #            " ORDER BY transact.bankaccount_id").params(category_id=category_id)
        
        stmt = text("SELECT * FROM transact"
                    " LEFT JOIN bankaccount ON transact.bankaccount_id = bankaccount_id"
                    " WHERE transact.category_id = :category_id"
                    " ORDER BY transact.bankaccount_id").params(category_id=category_id)

        res = db.engine.execute(stmt)
        response = []

        for r in res:
            print(r)
            response.append({
                "transaction_id": r[0],
                "account_name": r[16],
                "account_id": r[11],
                "amount": r[8],
                "credit_or_debit": r[11],
                "booking_date": r[3]
            })
        return response