from datetime import datetime
from app import db


class RentalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rented_from = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    rented_to = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    total_price = db.Column(db.Float, default=0.0)

    def serialize(self):
        """Custom Serializer"""
        return {
            "id": self.id,
            "car_id": self.car_id,
            "user_id": self.user_id,
            "rented_from": self.rented_from,
            "rented_to": self.rented_to,
            "total_price": self.total_price
        }

    def __repr__(self):
        return '<Rental History: {} rented by User {} from {} to {}>'.format(self.car_id,
                                                                             self.user_id,
                                                                             self.rented_from,
                                                                             self.rented_to)
