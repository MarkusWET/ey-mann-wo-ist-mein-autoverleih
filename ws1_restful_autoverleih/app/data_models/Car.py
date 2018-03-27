from datetime import datetime
from app import db


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(140))
    model = db.Column(db.String(140))
    price_per_day = db.Column(db.Float)

    def __repr__(self):
        return '<Car: {} {}>'.format(self.company, self.model)
