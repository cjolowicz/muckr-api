"""The API root."""
import flask

import muckr


blueprint = flask.Blueprint("main", __name__)


@blueprint.route("/")
def index():
    return "muckr API {version}".format(version=muckr.__version__)
