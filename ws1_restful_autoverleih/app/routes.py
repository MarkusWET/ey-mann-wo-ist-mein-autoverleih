from app import app, db, auth
from app.data_models.User import User
from app.data_models.LoanHistory import LoanHistory
from app.data_models.Car import Car
from datetime import datetime
from flask import abort, request, jsonify, g, url_for, escape, Response


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


@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username)
    user.hash_password(password)
    # TODO @markuswet: refactor to implement PBKDF2 with Salt and Iterations
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', user_id=user.id, _external=True)})


@app.route('/api/users/<user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(400)  # TODO @markuswet: is 400 BAD REQUEST really a good Status Code for data not found?
    return jsonify({'username': user.username})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)  # TODO @markuswet: Discuss with @mweber if duration is long/short enough
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@app.route("/api/car/loan", methods=["POST"])
# @auth.login_required
def loan_car():
    error_msg = ""
    error = False
    loan_end_date = "1901-01-01"
    loan_start_date = "1901-01-01"
    car_id = 1

    try:
        car_id = int(request.json.get("id"))
    except ValueError:
        error = True
        error_msg += "ID must be a number"

    try:
        loan_start_date = datetime.strptime(request.json.get("start"), "%Y-%m-%d")
    except ValueError:
        error = True
        error_msg += "Start date does not match the required format of \"YYYY-MM-DD\""

    try:
        loan_end_date = datetime.strptime(request.json.get("end"), "%Y-%m-%d")
    except ValueError:
        error = True
        error_msg += "end date does not match the required format of \"YYYY-MM-DD\""

    if error:
        abort(Response(escape(error_msg)))

    car = Car.query.get(car_id)
    loan_history = LoanHistory.query.filter_by(car_id=car.id, loaned_to=None).first()

    if loan_history is None:
        abort(404) # TODO @markuswet: Re-write the Error Message (currently: URL not found)
    # return escape("DEBUG: {} angefragt von {} bis {}".format(car, loan_start_date, loan_end_date))
