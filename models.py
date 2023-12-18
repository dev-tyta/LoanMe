from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50))
    email = db.Column(db.String(150))
    telephone = db.Column(db.String(20))
    password = db.Column(db.String(70))  # Consider using a hashing library here

    def __repr__(self):
        return f"<User {self.username}>"


class ApplicationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10))  # Kept as string for flexibility
    married = db.Column(db.String(10))
    dependent = db.Column(db.String(5))
    self_employed = db.Column(db.String(20))
    educated = db.Column(db.String(50))
    income = db.Column(db.Float)
    co_income = db.Column(db.Float)
    loan_amount = db.Column(db.Float)
    loan_term = db.Column(db.Integer)  # Corrected type
    prop = db.Column(db.String(20))

    def __repr__(self):
        return f"<ApplicationData {self.id}>"
