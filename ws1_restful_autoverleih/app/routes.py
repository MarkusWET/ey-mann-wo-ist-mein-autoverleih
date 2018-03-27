from app import app, db, auth
from app.data_models.User import User
from app.data_models.LoanHistory import LoanHistory
from app.data_models.Car import Car
from flask import abort, request, jsonify, g, url_for


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
        abort(400) # TODO @markuswet: is 400 BAD REQUEST really a good Status Code for data not found?
    return jsonify({'username': user.username})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600) # TODO @markuswet: Discuss with @mweber if duration is long/short enough
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})
