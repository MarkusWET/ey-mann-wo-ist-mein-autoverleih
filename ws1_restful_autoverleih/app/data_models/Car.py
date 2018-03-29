from datetime import datetime
from app import db


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(140))
    model = db.Column(db.String(140))
    price_per_day = db.Column(db.Float)
    gps_lat = db.Column(db.Float, default=0.0)
    gps_long = db.Column(db.Float, default=0.0)
    color = db.Column(db.String(7))
    rented = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            "id": self.id,
            "company": self.company,
            "model": self.model,
            "price_per_day": self.price_per_day,
            "gps_lat": self.gps_lat,
            "gps_long": self.gps_long,
            "color": self.color,
            "rented": self.rented
        }

    def __repr__(self):
        return '<Car: {} {}>'.format(self.company, self.model)
