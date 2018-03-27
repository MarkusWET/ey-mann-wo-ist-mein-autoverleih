from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    loans = db.relationship('Car', backref='lender', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(140))
    model = db.Column(db.String(140))
    price_per_day = db.Column(db.Float)
    loaned_from = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    loaned_to = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Car {}>'.format(self.body)
