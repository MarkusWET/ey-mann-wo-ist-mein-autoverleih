#!/usr/bin/env python
import os
from app import app, routes, db
from datetime import datetime, timedelta
from app.data_models.User import User
from app.data_models.Car import Car
from app.data_models.RentalHistory import RentalHistory


def init_db():
    # Create Demo User
    demo_user = User(username="test_user")
    demo_user.hash_password("test_pass")
    # TODO @markuswet: refactor to implement PBKDF2 with Salt and Iterations
    db.session.add(demo_user)
    db.session.commit()

    # Create Demo Cars
    demo_mustang = Car(company="Ford",
                       model="Mustang",
                       price_per_day=150.0,
                       gps_lat=48.213024,
                       gps_long=16.384843,
                       color="#0088CC")
    db.session.add(demo_mustang)

    demo_lada = Car(company="Lada",
                    model="Taiga",
                    price_per_day=10.0,
                    gps_lat=48.213024,
                    gps_long=16.384843,
                    color="#50191F")
    db.session.add(demo_lada)

    demo_enzo = Car(company="Ferrari",
                    model="Enzo",
                    price_per_day=6000.0,
                    gps_lat=48.213024,
                    gps_long=16.384843,
                    color="#FF2800")  # the real Ferrari red <3
    db.session.add(demo_enzo)

    db.session.commit()

    # Create Demo Rental
    demo_rental = RentalHistory(car_id=1,
                                user_id=1,
                                rented_from=datetime.today(),
                                rented_to=datetime.today() + timedelta(days=10),
                                total_price=demo_mustang.price_per_day * 10,
                                returned=False)
    db.session.add(demo_rental)

    demo_rental = RentalHistory(car_id=2,
                                user_id=1,
                                rented_from=datetime.today() - timedelta(days=15),
                                rented_to=datetime.today() - timedelta(days=1),
                                total_price=demo_lada.price_per_day * 10,
                                returned=False)
    db.session.add(demo_rental)

    demo_rental = RentalHistory(car_id=3,
                                user_id=1,
                                rented_from=datetime.today() + timedelta(days=10),
                                rented_to=datetime.today() + timedelta(days=375),
                                total_price=demo_enzo.price_per_day * 365,
                                returned=False)
    db.session.add(demo_rental)
    db.session.commit()


if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(ROOT_DIR, "app", "db.sqlite")

    if not os.path.exists(DB_PATH):
        db.create_all()
        init_db()

    app.run(debug=True)
