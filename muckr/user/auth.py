'''User authentication.'''
import flask
from flask_httpauth import HTTPBasicAuth

from muckr.user.models import User
from muckr.errors import error_response

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    flask.g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)
