import flask

from muckr.user.models import User, UserSchema
from muckr.extensions import database


blueprint = flask.Blueprint('user', __name__)


def jsonify(data):
    response = flask.jsonify(data)
    response.mimetype = 'application/vnd.api+json'
    return response


@blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    data, errors = UserSchema().dump(user)
    if errors:
        return jsonify(errors), 500
    return jsonify(data)


@blueprint.route('/users', methods=['POST'])
def create_user():
    schema = UserSchema()
    json = flask.request.get_json() or {}

    data, errors = schema.load(json)
    if errors:
        return jsonify(errors), 422

    user = User(**data)
    database.session.add(user)
    database.session.commit()

    data, errors = schema.dump(user)
    if errors:
        return jsonify(errors), 500

    response = jsonify(data)
    response.status_code = 201
    response.headers['Location'] = flask.url_for('user.get_user', id=user.id)
    return response
