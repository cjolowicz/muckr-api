"""User authentication."""
import flask
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from muckr.user.models import User
from muckr.errors import APIError

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    flask.g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    return APIError(401).handle()


@token_auth.verify_token
def verify_token(token):
    flask.g.current_user = User.check_token(token) if token else None
    return flask.g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    return APIError(401).handle()
