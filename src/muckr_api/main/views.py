"""The API root."""
import flask

import muckr_api


blueprint = flask.Blueprint("main", __name__)


@blueprint.route("/")
def index():
    return "muckr_api {version}".format(version=muckr_api.__version__)
