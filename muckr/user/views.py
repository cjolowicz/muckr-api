import flask

from muckr.user.models import User, UserSchema


blueprint = flask.Blueprint('user', __name__)


def jsonify(data):
    response = flask.jsonify(data)
    response.mimetype = 'application/vnd.api+json'
    return response


@blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    data, errors = UserSchema().dump(user)
    return jsonify(data)
