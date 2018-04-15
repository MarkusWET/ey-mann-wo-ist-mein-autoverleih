#!/usr/bin/env python
import os
from definitions import DB_PATH
from flask import Flask
from flask_misaka import Misaka
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from flask_cors import CORS

# initialization
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
md = Misaka()
basic_auth = HTTPBasicAuth()


def create_app():
    # FYI: AWS ElaticBeanstalk needs the app to be called "application".
    # The starting script also has to be called "application.py"
    application = Flask(__name__, template_folder="../templates")

    # TODO @markuswet: look into secure config for key
    application.config["SECRET_KEY"] = "the quick brown fox jumps over the lazy dog"
    application.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
    application.config["CURRENCY_CONVERTER_WSDL"] = \
        "http://currencyconverterservice-dev.eu-central-1.elasticbeanstalk.com/CurrencyService.svc?wsdl"

    # DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db.sqlite")
    application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(DB_PATH)

    # extensions
    db.init_app(application)
    migrate.init_app(application, db)
    cors.init_app(application, resources={r"/*": {"origins": "*"}})
    md.init_app(application)

    # init db
    if not os.path.exists(DB_PATH):
        db.create_all()
        # TODO @markuswet: re-initialize DB if not present. Current problem: circular dependency with data_models
        # init_db()

    # register routes
    from app.main import bp as main_bp
    application.register_blueprint(main_bp, url_prefix="/api")

    from app.errors import bp as errors_bp
    application.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    application.register_blueprint(auth_bp, url_prefix="/auth")

    return application

# def init_db():
#     # Create Demo User
#     demo_user = User(username="test_user")
#     demo_user.hash_password("test_pass")
#     # TODO @markuswet: refactor to implement PBKDF2 with Salt and Iterations
#     db.session.add(demo_user)
#     db.session.commit()
#
#     # Create Demo Cars
#     demo_mustang = Car(company="Ford",
#                        model="Mustang",
#                        price_per_day=150.0,
#                        gps_lat=48.213024,
#                        gps_long=16.384843,
#                        color="#0088CC",
#                        image_path="mustang.JPG")
#     db.session.add(demo_mustang)
#
#     demo_lada = Car(company="Lada",
#                     model="Taiga",
#                     price_per_day=10.0,
#                     gps_lat=48.213024,
#                     gps_long=16.384843,
#                     color="#50191F",
#                     image_path="lada.jpg")
#     db.session.add(demo_lada)
#
#     demo_enzo = Car(company="Ferrari",
#                     model="Enzo",
#                     price_per_day=6000.0,
#                     gps_lat=48.213024,
#                     gps_long=16.384843,
#                     color="#FF2800",
#                     image_path="ferrari.jpg")  # the real Ferrari red <3
#     db.session.add(demo_enzo)
#
#     db.session.commit()
#
#     # Create Demo Rental
#     demo_rental = RentalHistory(car_id=1,
#                                 user_id=1,
#                                 rented_from=datetime.today(),
#                                 rented_to=datetime.today() + timedelta(days=10),
#                                 total_price=demo_mustang.price_per_day * 10,
#                                 returned=False)
#     db.session.add(demo_rental)
#
#     demo_rental = RentalHistory(car_id=2,
#                                 user_id=1,
#                                 rented_from=datetime.today() - timedelta(days=15),
#                                 rented_to=datetime.today() - timedelta(days=1),
#                                 total_price=demo_lada.price_per_day * 10,
#                                 returned=False)
#     db.session.add(demo_rental)
#
#     demo_rental = RentalHistory(car_id=3,
#                                 user_id=1,
#                                 rented_from=datetime.today() + timedelta(days=10),
#                                 rented_to=datetime.today() + timedelta(days=375),
#                                 total_price=demo_enzo.price_per_day * 365,
#                                 returned=False)
#     db.session.add(demo_rental)
#     db.session.commit()
