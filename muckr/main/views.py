'''The root of the web service.'''
import flask


blueprint = flask.Blueprint('main', __name__)


@blueprint.route('/')
def index():
    return 'Hello, world!'
