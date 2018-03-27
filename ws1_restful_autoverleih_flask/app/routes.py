from flask import render_template, request, make_response
from functools import wraps
from datetime import datetime
from app import app


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
    car_id = request.args.get("id", default=1, type=int)
    error_msg = ""
    error = False
    loan_start_date_raw = request.args.get("start", default='1901-01-01', type=str)

    try:
        loan_start_date = datetime.strptime(loan_start_date_raw, "%Y-%m-%d")
    except ValueError as e:
        error = True
        error_msg += "Start date does not match the required format of \"YYYY-MM-DD\""

    loan_end_date_raw = request.args.get("end", default='1901-01-01', type=str)

    try:
        loan_end_date = datetime.strptime(loan_end_date_raw, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        error = True
        error_msg += "end date does not match the required format of \"YYYY-MM-DD\""

    if error:
        return error_msg

    return "auto {} ausgeliehen von {} bis {}".format(car_id, loan_start_date, loan_end_date)


@app.route("/car/return")
@auth_required
def return_car():
    car_id = request.args.get("id", default=1, type=int)
    return "auto {} zurückgegeben".format(car_id)

#
# if __name__ == '__main__':
#     app.run()
