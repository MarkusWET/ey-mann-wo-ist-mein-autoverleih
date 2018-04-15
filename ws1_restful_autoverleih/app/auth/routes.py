from application import db
from app.auth import bp
from app.data_models.User import User
from flask import abort, request, jsonify, url_for, Response
from sqlalchemy import exc


@bp.route("/api/users", methods=["POST"])
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
