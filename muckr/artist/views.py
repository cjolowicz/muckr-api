'''Artist views.'''
import flask
from marshmallow import ValidationError

from muckr.errors import APIError
from muckr.extensions import database
from muckr.user.auth import token_auth
from muckr.artist.models import Artist, ArtistSchema
from muckr.utils import jsonify, check_unique_on_create, check_unique_on_update


blueprint = flask.Blueprint('artist', __name__)
artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)


@blueprint.route('/artists', methods=['GET'])
@token_auth.login_required
def get_artists():
    page = flask.request.args.get('page', 1, type=int)
    per_page = min(flask.request.args.get('per_page', 10, type=int), 100)
    artists = flask.g.current_user.artists.paginate(page, per_page, False)
    data, errors = artists_schema.dump(artists.items)

    return jsonify(data)


@blueprint.route('/artists/<int:id>', methods=['GET'])
@token_auth.login_required
def get_artist(id):
    artist = Artist.query.get_or_404(id)
    if artist.user.id != flask.g.current_user.id:
        raise APIError(404)
    data, errors = artist_schema.dump(artist)

    return jsonify(data)


@blueprint.route('/artists', methods=['POST'])
@token_auth.login_required
def create_artist():
    json = flask.request.get_json() or {}

    try:
        data, errors = artist_schema.load(json)
    except ValidationError as error:
        raise APIError(422, details=error.messages)

    check_unique_on_create(flask.g.current_user.artists, data, ['name'])

    artist = Artist(**data)
    artist.user = flask.g.current_user

    database.session.add(artist)
    database.session.commit()

    data, errors = artist_schema.dump(artist)

    response = jsonify(data)
    response.status_code = 201
    response.headers['Location'] = flask.url_for(
        'artist.get_artist', id=artist.id)
    return response


@blueprint.route('/artists/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_artist(id):
    if not flask.g.current_user.is_admin:
        raise APIError(401)

    artist = Artist.query.get_or_404(id)
    json = flask.request.get_json() or {}

    try:
        data, errors = ArtistSchema(partial=True).load(json)
    except ValidationError as error:
        raise APIError(422, details=error.messages)

    check_unique_on_update(Artist.query, artist, data, ['name'])

    for key, value in data.items():
        setattr(artist, key, value)

    database.session.commit()

    data, errors = ArtistSchema().dump(artist)
    return jsonify(data)


@blueprint.route('/artists/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_artist(id):
    artist = Artist.query.get_or_404(id)
    if artist.user.id != flask.g.current_user.id:
        raise APIError(404)

    database.session.delete(artist)
    database.session.commit()

    return jsonify({}), 204
