from flask import render_template, request, make_response, escape
from functools import wraps
from datetime import datetime
from app import app
from app.data_models import Car, User


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html")


def auth_required(f):
    # This could also be done via Flask-Login etc.
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.authorization and request.authorization.username == "un" and request.authorization.password == "pw":
            return f(*args, **kwargs)

        return make_response("(401) Unauthorized", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'})

    return decorated


@app.route("/")
@app.route("/index")
def hello_world():
    return render_template("home.html")


@app.route("/car/loan")
@auth_required
def loan_car():
    error_msg = ""
    error = False
    loan_end_date = "1901-01-01"
    loan_start_date = "1901-01-01"
    car_id = 1

    try:
        car_id = int(request.args.get("id", default=1, type=int))
    except ValueError:
        error = True
        error_msg += "ID must be a number"

    try:
        loan_start_date = datetime.strptime(request.args.get("start", default='1901-01-01', type=str), "%Y-%m-%d")
    except ValueError:
        error = True
        error_msg += "Start date does not match the required format of \"YYYY-MM-DD\""

    try:
        loan_end_date = datetime.strptime(request.args.get("end", default='1901-01-01', type=str), "%Y-%m-%d")
    except ValueError:
        error = True
        error_msg += "end date does not match the required format of \"YYYY-MM-DD\""

    if error:
        return error_msg

    car = Car.query.get(car_id)

    return escape("DEBUG: {} angefragt von {} bis {}".format(car, loan_start_date, loan_end_date))


@app.route("/car/return")
@auth_required
def return_car():
    car_id = request.args.get("id", default=1, type=int)
    return "DEBUG: auto {} zurückgegeben".format(car_id)
