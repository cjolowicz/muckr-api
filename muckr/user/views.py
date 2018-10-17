import flask

from muckr.user.models import User, UserSchema


blueprint = flask.Blueprint('user', __name__)


@blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    data, errors = UserSchema().dumps(user)
    return data
