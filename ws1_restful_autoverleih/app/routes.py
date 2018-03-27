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
    token = g.user.generate_auth_token(600)  # TODO @markuswet: Discuss with @mweber if duration is long/short enough
    return jsonify({"token": token.decode("ascii"), "duration": 600})


@app.route("/api/resource")
@auth.login_required
def get_resource():
    return jsonify({"data": "Hello, %s!" % g.user.username})


@app.route("/api/car/rent", methods=["POST"])
# @auth.login_required
def rent_car():
    error_msg = ""
    error = False
    rental_start_date = "1901-01-01"
    rental_end_date = "1901-01-01"
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

    try:
        rental_start_date = datetime.strptime(request.json.get("start"), "%Y-%m-%d")
    except ValueError:
        error = True
        error_msg += "Start date does not match the required format of \"YYYY-MM-DD\""

    try:
        rental_end_date = datetime.strptime(request.json.get("end"), "%Y-%m-%d")
        rental_end_date = rental_end_date + timedelta(days=1, seconds=-1)
    except ValueError:
        error = True
        error_msg += "end date does not match the required format of \"YYYY-MM-DD\""

    car = Car.query.get(car_id)
    if car is None:
        error = True
        error_msg += "Car with ID {} not found".format(car_id)

    user = User.query.get(user_id)
    if user is None:
        error = True
        error_msg += "User with ID {} not found".format(user)

    if error:
        abort(Response(escape(error_msg)))

    rental_history = db.session.query(RentalHistory). \
        filter(RentalHistory.car_id == 1, RentalHistory.rented_to >= rental_start_date). \
        order_by(RentalHistory.rented_to.desc()). \
        first()

    if rental_history is None:
        duration = rental_end_date - rental_start_date
        total = car.price_per_day * duration.days
        rental = RentalHistory(car_id=car.id,
                               user_id=user.id,
                               rented_from=rental_start_date,
                               rented_to=rental_end_date,
                               total_price=total)
        db.session.add(rental)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            abort(Response("Query unsuccessful. Changes rolled back", 500))

    else:
        abort(Response("Car {} already rented in that timeframe.".format(car.id)))
