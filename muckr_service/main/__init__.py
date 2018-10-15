import flask

blueprint = flask.Blueprint('main', __name__)

import muckr_service.main.routes
