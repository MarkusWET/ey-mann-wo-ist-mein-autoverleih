from app import app, db, auth
from app.currency_exchange import convert_from_eur, convert_to_eur
from app.data_models.User import User
from app.data_models.RentalHistory import RentalHistory
from app.data_models.Car import Car
from datetime import datetime, timedelta
from flask import abort, request, jsonify, g, url_for, escape, Response
from sqlalchemy import exc, exists, and_


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

    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        db.session.rollback()
        abort(Response("Query unsuccessful. Changes rolled back.\n", 500))

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


@app.route("/api/car/<car_id>/rent", methods=["PUT"])
@auth.login_required
def rent_car(car_id):
    """Rent car with id car_id for the dates (YYYY-MM-DD) defined in the body with start and end"""
    rental_start_date = "1901-01-01"
    rental_end_date = "1901-01-01"

    try:
        car_id = int(car_id)
    except ValueError:
        abort(Response("Car ID must be a number\n", 400))

    # Try to find user
    user = User.query.get(g.user.id)
    if user is None:
        abort(Response("Invalid user", 400))

    # Validate Dates
    try:
        rental_start_date = datetime.strptime(request.json.get("start"), "%Y-%m-%d")
    except ValueError:
        abort(Response("Start date does not match the required format of \"YYYY-MM-DD\"\n", 400))

    try:
        rental_end_date = datetime.strptime(request.json.get("end"), "%Y-%m-%d")
        rental_end_date = rental_end_date + timedelta(days=1, seconds=-1)
    except ValueError:
        abort(Response("End date does not match the required format of \"YYYY-MM-DD\"\n", 400))

    # Try to find car
    car = Car.query.get(car_id)
    if car is None:
        abort(Response("Car with ID {} not found.\n".format(car), 404))

    # Get all car_ids that are rented in the timeframe
    rentals_subquery = db.session.query(RentalHistory.car_id). \
        filter(RentalHistory.rented_from < rental_end_date,
               RentalHistory.rented_to > rental_start_date,
               RentalHistory.returned.isnot(True)). \
        subquery()

    # get all cars that are not in the rented car_ids
    available_cars = db.session.query(Car). \
        filter(~Car.id.in_(rentals_subquery)). \
        all()

    if car not in available_cars:
        abort(Response("Car {} not available during the defined timeframe!".format(car.id), 409))
    else:
        duration = rental_end_date - rental_start_date
        total = car.price_per_day * duration.days
        rental = RentalHistory(car_id=car.id,
                               user_id=user.id,
                               rented_from=rental_start_date,
                               rented_to=rental_end_date,
                               total_price=total,
                               returned=False)
        db.session.add(rental)

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            abort(Response("Query unsuccessful. Changes rolled back.\n", 500))

        return Response("Car {} rented successfully.\n".format(car.id), 200)


@app.route("/api/car/<car_id>/return", methods=["PUT"])
@auth.login_required
def return_car(car_id):
    # TODO @markuswet (optional): add column return_date and calculate the difference between booked return and actual return as late fee

    try:
        car_id = int(car_id)
    except ValueError:
        abort(Response("Car ID must be a number\n", 400))

    # Try to find car
    car = Car.query.get(car_id)
    if car is None:
        abort(Response("Car with ID {} not found.\n".format(car), 404))

    rental = db.session.query(RentalHistory). \
        filter(RentalHistory.car_id == car_id,
               RentalHistory.user_id == g.user.id,
               RentalHistory.returned.isnot(True)). \
        first()

    if rental is None:
        abort(Response("No valid rental found to return.\n", 400))

    rental.returned = True

    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        db.session.rollback()
        abort(Response("Query unsuccessful. Changes rolled back.\n", 500))

    return Response("Car with ID {} returned successfully.".format(car_id), 200)


@app.route("/api/car/available", methods=["PUT"])
@auth.login_required
def get_available_cars():
    rental_start_date = "1901-01-01"
    rental_end_date = "1901-01-01"

    # Validate Date
    try:
        rental_start_date = datetime.strptime(request.json.get("start"), "%Y-%m-%d")
    except ValueError:
        abort(Response("Start date does not match the required format of \"YYYY-MM-DD\"\n", 400))

    try:
        rental_end_date = datetime.strptime(request.json.get("end"), "%Y-%m-%d")
        rental_end_date = rental_end_date + timedelta(days=1, seconds=-1)
    except ValueError:
        abort(Response("End date does not match the required format of \"YYYY-MM-DD\"\n", 400))

    # Rental History Logic
    #  -- powered by: way smarter brains @ StackOverflow:
    #  -- https://stackoverflow.com/questions/6111263/sql-scheduling-select-all-rooms-available-for-given-date-range/6111388#6111388
    # Select * From Car c
    # where not exists
    #     (Select * From RentalHistory
    #     Where car_id = c.id
    #         And RentalHistory.rented_from < rental_end_date
    #         And RentalHistory.rented_to > rental_start_date)

    # Get all car_ids that are rented in the timeframe
    rentals_subquery = db.session.query(RentalHistory.car_id). \
        filter(RentalHistory.rented_from < rental_end_date, RentalHistory.rented_to > rental_start_date). \
        subquery()

    # get all cars that are not in the rented car_ids
    available = db.session.query(Car). \
        filter(~Car.id.in_(rentals_subquery)). \
        all()
    db.session.close()

    if len(available) < 1:
        abort(Response("No cars available!", 404))

    # TODO @markuswet: refactor recalculation into own method
    # Re-calculate prices in target currency
    target_currency = request.args.get("currency")

    if target_currency != "EUR":
        for car in available:
            car.price_per_day = convert_from_eur(target_currency, str(car.price_per_day))
    return jsonify(available=[e.serialize() for e in available])


@app.route("/api/car/all")
def get_all_cars():
    all_cars = db.session.query(Car).all()
    db.session.close()
    if all_cars is None:
        abort(Response("No cars found!", 500))

    # TODO @markuswet: refactor recalculation into own method
    # Re-calculate prices in target currency
    target_currency = request.args.get("currency")

    if target_currency != "EUR":
        for car in all_cars:
            car.price_per_day = convert_from_eur(target_currency, str(car.price_per_day))
    return jsonify(available=[e.serialize() for e in all_cars])


@app.route("/api/user/<user_id>/rented")
@auth.login_required
def get_rented_cars_of_user(user_id):
    uid = 0

    try:
        uid = int(user_id)
    except ValueError:
        abort(Response("User ID must be a number\n", 400))

    if uid != g.user.id:
        abort(Response("User ID does not match Token User ID!", 400))

    # Try to find user
    user = User.query.get(g.user.id)
    if user is None:
        abort(Response("Invalid user", 400))

    rented_cars = db.session.query(RentalHistory). \
        filter(RentalHistory.user_id == uid, RentalHistory.returned.isnot(True)). \
        all()
    db.session.close()

    if len(rented_cars) < 1:
        abort(Response("No rented cars for User {} found".format(uid), 200))

    # TODO @markuswet: refactor recalculation into own method
    # Re-calculate prices in target currency
    target_currency = request.args.get("currency")

    if target_currency != "EUR":
        for car in rented_cars:
            car.price_per_day = convert_from_eur(target_currency, str(car.price_per_day))

    return jsonify(rentals=[e.serialize() for e in rented_cars])
