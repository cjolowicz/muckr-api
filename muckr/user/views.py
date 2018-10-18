import flask

from muckr.user.models import User, UserSchema
from muckr.extensions import database


blueprint = flask.Blueprint('user', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


def _jsonify(data):
    response = flask.jsonify(data)
    response.mimetype = 'application/vnd.api+json'
    return response


@blueprint.route('/users', methods=['GET'])
def get_users():
    page = flask.request.args.get('page', 1, type=int)
    per_page = min(flask.request.args.get('per_page', 10, type=int), 100)
    users = User.query.paginate(page, per_page, False)
    data, errors = users_schema.dump(users.items)
    if errors:
        return _jsonify(errors), 500
    return _jsonify(data)


@blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    data, errors = user_schema.dump(user)
    if errors:
        return _jsonify(errors), 500
    return _jsonify(data)


@blueprint.route('/users', methods=['POST'])
def create_user():
    json = flask.request.get_json() or {}
    data, errors = user_schema.load(json)
    if errors:
        return _jsonify(errors), 422

    password = data.pop('password', None)
    user = User(**data)
    if password is not None:
        user.set_password(password)

    database.session.add(user)
    database.session.commit()

    data, errors = user_schema.dump(user)
    if errors:
        return _jsonify(errors), 500

    response = _jsonify(data)
    response.status_code = 201
    response.headers['Location'] = flask.url_for('user.get_user', id=user.id)
    return response
