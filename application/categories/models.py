from application import db

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