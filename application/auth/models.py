from application import db
from application.models import Base

class User(Base):
    __tablename__ = "account"

    name=db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    bankaccounts = db.relationship("BankAccount", backref="bankaccount", lazy =True)
    categories = db.relationship("Category", backref="category", lazy=True)

    role = db.Column(db.String(15), nullable=False)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
    
    def get_id(self):
        return self.id

    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True

    def get_role(self):
        return self.role