from app import app, db, auth
from app.data_models.User import User
from app.data_models.RentalHistory import RentalHistory
from app.data_models.Car import Car
from datetime import datetime, timedelta
from flask import abort, request, jsonify, g, url_for, escape, Response
from sqlalchemy import exc


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route("/api/users", methods=["POST"])
def new_user():
    username = request.json.get("username")
    password = request.json.get("password")
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username)
    user.hash_password(password)
    # TODO @markuswet: refactor to implement PBKDF2 with Salt and Iterations
    db.session.add(user)
    db.session.commit()
    return (jsonify({"username": user.username}), 201,
            {"Location": url_for("get_user", user_id=user.id, _external=True)})


@app.route("/api/users/<user_id>")
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(400)  # TODO @markuswet: is 400 BAD REQUEST really a good Status Code for data not found?
    return jsonify({"username": user.username})


@app.route("/api/token")
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(60000)  # TODO @markuswet: Discuss with @mweber if duration is long/short enough
    return jsonify({"token": token.decode("ascii"), "duration": 60000})


@app.route("/api/resource")
@auth.login_required
def get_resource():
    return jsonify({"data": "Hello, %s!" % g.user.username})


@app.route("/api/car/<car_id>/rent", methods=["PUT"])
@auth.login_required
def rent_car(car_id):
    """Rent car with id car_id for the dates (YYYY-MM-DD) defined in the body with start and end"""
    rental_start_date = "1901-01-01"
    rental_end_date = "1901-01-01"

    # Try to find user
    user = User.query.get(g.user.id)
    if user is None:
        abort(Response("Invalid user", 400))

    # Validate Dates
    try:
        rental_start_date = datetime.strptime(request.json.get("start"), "%Y-%m-%d")
    except ValueError:
        abort(Response("Start date does not match the required format of \"YYYY-MM-DD\"\n"), 400)

    try:
        rental_end_date = datetime.strptime(request.json.get("end"), "%Y-%m-%d")
        rental_end_date = rental_end_date + timedelta(days=1, seconds=-1)
    except ValueError:
        abort(Response("End date does not match the required format of \"YYYY-MM-DD\"\n"), 400)

    # Try to find car
    car = Car.query.get(car_id)
    if car is None:
        abort(Response("Car with ID {} not found.\n".format(car)), 404)

    rental = db.session.query(RentalHistory). \
        filter(RentalHistory.car_id == 1, RentalHistory.rented_to >= rental_start_date). \
        order_by(RentalHistory.rented_to.desc()). \
        first()

    if rental is None:
        duration = rental_end_date - rental_start_date
        total = car.price_per_day * duration.days
        rental = RentalHistory(car_id=car.id,
                               user_id=user.id,
                               rented_from=rental_start_date,
                               rented_to=rental_end_date,
                               total_price=total)
        db.session.add(rental)

        car.rented = True

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            abort(Response("Query unsuccessful. Changes rolled back.\n", 500))

        return jsonify(rental_entry=rental.serialize())
    else:
        abort(Response("Car {} already rented in that timeframe.\n".format(car.id), 409))


@app.route("/api/car/<car_id>/return", methods=["PUT"])
@auth.login_required
def return_car(car_id):
    error_msg = ""
    error = False
    car_id = 0
    user_id = 0

    try:
        car_id = int(request.json.get("car"))
    except ValueError:
        error = True
        error_msg += "Car ID must be a number"
    try:
        user_id = int(request.json.get("user"))
    except ValueError:
        error = True
        error_msg += "User ID must be a number"

    rental = db.session.query(RentalHistory). \
        filter(RentalHistory.car_id == car_id, RentalHistory.user_id == user_id). \
        order_by(RentalHistory.rented_to.desc()). \
        first()
    rental.returned = True

    car = db.session.query(Car). \
        filter(Car.id == car_id). \
        first()
    car.rented = False

    db.session.commit()


@app.route("/api/car/available")
@auth.login_required
def available_cars():
    available = db.session.query(Car). \
        filter(Car.rented.isnot(True)). \
        all()
    if available is None:
        abort(Response("No cars available!", 404))
    else:
        return jsonify(available=[e.serialize() for e in available])


@app.route("/api/user/<user_id>/rented")
@auth.login_required
def rented_cars(user_id):
    uid = 0

    try:
        uid = int(user_id)
    except ValueError:
        abort(400)

    if uid != g.user.id:
        abort(Response("User ID does not match Token User ID!", 400))
    user_cars = db.session.query(RentalHistory). \
        filter(RentalHistory.user_id == uid, RentalHistory.returned.isnot(True)). \
        all()

    return jsonify(rentals=[e.serialize() for e in user_cars])
