from datetime import datetime, timedelta
from flask import current_app, g
from flask.cli import with_appcontext
from app import db
from app.data_models.User import User
from app.data_models.RentalHistory import RentalHistory
from app.data_models.Car import Car


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    # if 'db' not in g:
    #     g.db = sqlite3.connect(
    #         current_app.config['DATABASE'],
    #         detect_types=sqlite3.PARSE_DECLTYPES
    #     )
    #     g.db.row_factory = sqlite3.Row

    return db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    # db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    # db = get_db()
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
                       color="#0088CC",
                       image_path="mustang.JPG")
    db.session.add(demo_mustang)

    demo_lada = Car(company="Lada",
                    model="Taiga",
                    price_per_day=10.0,
                    gps_lat=38.213024,
                    gps_long=26.384843,
                    color="#50191F",
                    image_path="lada.jpg")
    db.session.add(demo_lada)

    demo_enzo = Car(company="Ferrari",
                    model="Enzo",
                    price_per_day=6000.0,
                    gps_lat=28.213024,
                    gps_long=36.384843,
                    color="#FF2800",
                    image_path="ferrari.jpg")  # the real Ferrari red <3
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
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """Clear existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    # app.cli.add_command(init_db_command)
