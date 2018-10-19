'''User views.'''
import flask
from marshmallow import ValidationError

from muckr.errors import error_response
from muckr.extensions import database
from muckr.user.auth import basic_auth, token_auth
from muckr.user.models import User, UserSchema


blueprint = flask.Blueprint('user', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


def _jsonify(data):
    response = flask.jsonify(data)
    response.mimetype = 'application/json'
    return response


@blueprint.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    if not flask.g.current_user.is_admin:
        return error_response(401)
    page = flask.request.args.get('page', 1, type=int)
    per_page = min(flask.request.args.get('per_page', 10, type=int), 100)
    users = User.query.paginate(page, per_page, False)
    data, errors = users_schema.dump(users.items)
    return _jsonify(data)


@blueprint.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    user = User.query.get_or_404(id)
    if user.id != flask.g.current_user.id:
        return error_response(401)

    data, errors = user_schema.dump(user)
    return _jsonify(data)


@blueprint.route('/users', methods=['POST'])
def create_user():
    json = flask.request.get_json() or {}
    try:
        data, errors = user_schema.load(json)
    except ValidationError as error:
        return error_response(422, details=error.messages)

    for key in ['username', 'email']:
        condition = {key: data[key]}
        if User.query.filter_by(**condition).first():
            message = 'please use a different {key}'.format(key=key)
            return error_response(400, message=message, details={key: message})

    password = data.pop('password', None)
    user = User(**data)
    if password is not None:
        user.set_password(password)

    database.session.add(user)
    database.session.commit()

    data, errors = user_schema.dump(user)

    response = _jsonify(data)
    response.status_code = 201
    response.headers['Location'] = flask.url_for('user.get_user', id=user.id)
    return response


@blueprint.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    user = User.query.get_or_404(id)
    if user.id != flask.g.current_user.id:
        return error_response(401)

    json = flask.request.get_json() or {}
    try:
        data, errors = UserSchema(partial=True).load(json)
    except ValidationError as error:
        return error_response(422, details=error.messages)

    for key in ['username', 'email']:
        if key in data and data[key] != getattr(user, key):
            condition = {key: data[key]}
            if User.query.filter_by(**condition).first():
                message = 'please use a different {key}'.format(key=key)
                return error_response(400, message=message,
                                      details={key: message})

    password = data.pop('password', None)
    if password is not None:
        user.set_password(password)

    for key, value in data.items():
        setattr(user, key, value)

    database.session.commit()

    data, errors = UserSchema().dump(user)
    return _jsonify(data)


@blueprint.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id != flask.g.current_user.id:
        return error_response(401)

    database.session.delete(user)
    database.session.commit()

    return _jsonify({}), 204


@blueprint.route('/tokens', methods=['POST'])
@basic_auth.login_required
def create_token():
    token = flask.g.current_user.get_token()
    database.session.commit()
    return _jsonify({'token': token}), 201


@blueprint.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def delete_token():
    flask.g.current_user.revoke_token()
    database.session.commit()
    return _jsonify({}), 204
