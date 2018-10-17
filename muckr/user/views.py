import flask

from muckr.user.models import User


blueprint = flask.Blueprint('user', __name__)


@blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return flask.jsonify(user.to_dict())
