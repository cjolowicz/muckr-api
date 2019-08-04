"""Venue views."""
import flask
from marshmallow import ValidationError

from muckr_api.errors import APIError
from muckr_api.extensions import database
from muckr_api.user.auth import token_auth
from muckr_api.venue.models import Venue, VenueSchema
from muckr_api.utils import (
    check_unique_on_create,
    check_unique_on_update,
    jsonify,
    paginate,
)


blueprint = flask.Blueprint("venue", __name__)
venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)


@blueprint.route("/venues", methods=["GET"])
@token_auth.login_required
def get_venues():
    venues = paginate(flask.g.current_user.venues)
    data = venues_schema.dump(venues.items)

    return jsonify(data)


@blueprint.route("/venues/<int:id>", methods=["GET"])
@token_auth.login_required
def get_venue(id):
    venue = Venue.query.get_or_404(id)
    if venue.user.id != flask.g.current_user.id and not flask.g.current_user.is_admin:
        raise APIError(404)
    data = venue_schema.dump(venue)

    return jsonify(data)


@blueprint.route("/venues", methods=["POST"])
@token_auth.login_required
def create_venue():
    json = flask.request.get_json() or {}

    try:
        data = venue_schema.load(json)
    except ValidationError as error:
        raise APIError(422, details=error.messages)

    check_unique_on_create(flask.g.current_user.venues, data, ["name"])

    venue = Venue(**data)
    venue.user = flask.g.current_user

    database.session.add(venue)
    database.session.commit()

    data = venue_schema.dump(venue)

    response = jsonify(data)
    response.status_code = 201
    response.headers["Location"] = flask.url_for("venue.get_venue", id=venue.id)
    return response


@blueprint.route("/venues/<int:id>", methods=["PUT"])
@token_auth.login_required
def update_venue(id):
    venue = Venue.query.get_or_404(id)
    if venue.user.id != flask.g.current_user.id and not flask.g.current_user.is_admin:
        raise APIError(404)

    json = flask.request.get_json() or {}

    try:
        data = VenueSchema(partial=True).load(json)
    except ValidationError as error:
        raise APIError(422, details=error.messages)

    check_unique_on_update(flask.g.current_user.venues, venue, data, ["name"])

    for key, value in data.items():
        setattr(venue, key, value)

    database.session.commit()

    data = VenueSchema().dump(venue)
    return jsonify(data)


@blueprint.route("/venues/<int:id>", methods=["DELETE"])
@token_auth.login_required
def delete_venue(id):
    venue = Venue.query.get_or_404(id)
    if venue.user.id != flask.g.current_user.id and not flask.g.current_user.is_admin:
        raise APIError(404)

    database.session.delete(venue)
    database.session.commit()

    return jsonify({}), 204
