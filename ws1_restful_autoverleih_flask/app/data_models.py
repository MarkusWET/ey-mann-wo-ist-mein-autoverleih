from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    pbkdf2_salt = db.Column(db.String(128))
    pbkdf2_iterations = db.Column(db.Integer)
    pbkdf2_hashed_pw = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(140))
    model = db.Column(db.String(140))
    price_per_day = db.Column(db.Float)

    def __repr__(self):
        return '<Car {}>'.format(self.body)


class LoanHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    loaned_from = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    loaned_to = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Loan History {}>'.format(self.body)
