from application import db
from sqlalchemy import text

class AccountCategory(db.Model):
    __tablename__ = "accountcategory"

    bankaccount_id = db.Column(db.Integer, db.ForeignKey('bankaccount.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key = True)

    @staticmethod
    def get_categories_by_account(bankaccount_id):
        stmt = text("SELECT * FROM bankaccount"
                    " LEFT JOIN category ON"
                    " ON accountcategory.bankaccount_id = bankaccount_id AND accountcategory.category_id = category.id"
                    " WHERE bankaccount_id = :bankaccount_id").params(bankaccount_id=bankaccount_id)

        res = db.engine.execute(stmt)
        response = []
        for r in res:
            print(r)