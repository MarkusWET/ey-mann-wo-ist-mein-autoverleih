from flask import render_template, request
from datetime import datetime
from app import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html")


@app.route("/")
@app.route("/index")
def hello_world():
    return render_template("home.html")


@app.route("/car/loan")
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
def return_car():
    car_id = request.args.get("id", default=1, type=int)
    return "auto {} zurückgegeben".format(car_id)

#
# if __name__ == '__main__':
#     app.run()
