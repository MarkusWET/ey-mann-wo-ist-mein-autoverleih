from datetime import datetime
from app import db


class LoanHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    loaned_from = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    loaned_to = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Loan History: {} loaned by User {} from {} to {}>'.format(self.car_id, self.user_id, self.loaned_from,
                                                                           self.loaned_to)
