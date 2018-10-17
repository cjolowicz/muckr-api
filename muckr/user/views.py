import flask

from muckr.user.models import User, UserSchema


blueprint = flask.Blueprint('user', __name__)


@blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    data, errors = UserSchema().dump(user)
    response = flask.jsonify(data)
    response.mimetype = 'application/vnd.api+json'
    return response
