import flask

from muckr.user.models import User, UserSchema
from muckr.extensions import database


blueprint = flask.Blueprint('user', __name__)


def _jsonify(data):
    response = flask.jsonify(data)
    response.mimetype = 'application/vnd.api+json'
    return response


@blueprint.route('/users', methods=['GET'])
def get_users():
    page = flask.request.args.get('page', 1, type=int)
    per_page = min(flask.request.args.get('per_page', 10, type=int), 100)
    users = User.query.paginate(page, per_page, False)
    data, errors = UserSchema(many=True).dump(users.items)
    if errors:
        return _jsonify(errors), 500
    return _jsonify(data)


@blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    data, errors = UserSchema().dump(user)
    if errors:
        return _jsonify(errors), 500
    return _jsonify(data)


@blueprint.route('/users', methods=['POST'])
def create_user():
    schema = UserSchema()
    json = flask.request.get_json() or {}

    user, errors = schema.load(json)
    if errors:
        return _jsonify(errors), 422

    database.session.add(user)
    database.session.commit()

    data, errors = schema.dump(user)
    if errors:
        return _jsonify(errors), 500

    response = _jsonify(data)
    response.status_code = 201
    response.headers['Location'] = flask.url_for('user.get_user', id=user.id)
    return response
