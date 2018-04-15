from app import db, basic_auth
from app.auth import bp
from app.data_models.User import User
from flask import abort, request, jsonify, url_for, Response
from sqlalchemy import exc


# route prefix "auth/"
@bp.route("/register", methods=["POST"])
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


@bp.route("/user/<user_id>")
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(400)  # TODO @markuswet: is 400 BAD REQUEST really a good Status Code for data not found?
    return jsonify({"username": user.username})


@bp.route("/token")
@basic_auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(60000)  # TODO @markuswet: Discuss with @mweber if duration is long/short enough
    return jsonify({"token": token.decode("ascii"), "duration": 60000})
