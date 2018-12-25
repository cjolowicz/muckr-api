"""User views."""
import flask
from marshmallow import ValidationError

from muckr.errors import APIError
from muckr.extensions import database
from muckr.user.auth import basic_auth, token_auth
from muckr.user.models import User, UserSchema
from muckr.utils import (
    check_unique_on_create,
    check_unique_on_update,
    jsonify,
    paginate,
)


blueprint = flask.Blueprint("user", __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@blueprint.route("/users", methods=["GET"])
@token_auth.login_required
def get_users():
    if not flask.g.current_user.is_admin:
        raise APIError(401)
    users = paginate(User.query)
    data = users_schema.dump(users.items)
    return jsonify(data)


@blueprint.route("/users/<int:id>", methods=["GET"])
@token_auth.login_required
def get_user(id):
    user = User.query.get_or_404(id)
    if user.id != flask.g.current_user.id and not flask.g.current_user.is_admin:
        raise APIError(401)

    data = user_schema.dump(user)
    return jsonify(data)


@blueprint.route("/users", methods=["POST"])
def create_user():
    json = flask.request.get_json() or {}
    try:
        data = user_schema.load(json)
    except ValidationError as error:
        raise APIError(422, details=error.messages)

    check_unique_on_create(User.query, data, ["username", "email"])

    password = data.pop("password", None)
    user = User(**data)
    if password is not None:
        user.set_password(password)

    database.session.add(user)
    database.session.commit()

    data = user_schema.dump(user)

    response = jsonify(data)
    response.status_code = 201
    response.headers["Location"] = flask.url_for("user.get_user", id=user.id)
    return response


@blueprint.route("/users/<int:id>", methods=["PUT"])
@token_auth.login_required
def update_user(id):
    user = User.query.get_or_404(id)
    if user.id != flask.g.current_user.id and not flask.g.current_user.is_admin:
        raise APIError(401)

    json = flask.request.get_json() or {}
    try:
        data = UserSchema(partial=True).load(json)
    except ValidationError as error:
        raise APIError(422, details=error.messages)

    check_unique_on_update(User.query, user, data, ["username", "email"])

    password = data.pop("password", None)
    if password is not None:
        user.set_password(password)

    for key, value in data.items():
        setattr(user, key, value)

    database.session.commit()

    data = UserSchema().dump(user)
    return jsonify(data)


@blueprint.route("/users/<int:id>", methods=["DELETE"])
@token_auth.login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id != flask.g.current_user.id and not flask.g.current_user.is_admin:
        raise APIError(401)

    database.session.delete(user)
    database.session.commit()

    return jsonify({}), 204


@blueprint.route("/tokens", methods=["POST"])
@basic_auth.login_required
def create_token():
    token = flask.g.current_user.get_token()
    database.session.commit()
    return jsonify({"token": token}), 201


@blueprint.route("/tokens", methods=["DELETE"])
@token_auth.login_required
def delete_token():
    flask.g.current_user.revoke_token()
    database.session.commit()
    return jsonify({}), 204
