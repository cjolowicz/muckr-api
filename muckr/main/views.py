'''The root of the web service.'''
import flask

import muckr


blueprint = flask.Blueprint('main', __name__)


@blueprint.route('/')
def index():
    return 'muckr-service {version}'.format(version=muckr.__version__)
