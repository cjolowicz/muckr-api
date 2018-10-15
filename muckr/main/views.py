import flask

import muckr.models # noqa


blueprint = flask.Blueprint('main', __name__)


@blueprint.route('/')
def index():
    return 'Hello, world!'
