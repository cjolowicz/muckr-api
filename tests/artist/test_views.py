'''Test artist views.'''
import json
import pytest

from muckr.artist.models import Artist
from muckr.artist.views import artist_schema, artists_schema

from tests.artist.factories import ArtistFactory


def _create_token_auth_header(token):
    return {'Authorization': 'Bearer {token}'.format(token=token)}


class TestGetArtists:
    def test_get_request_returns_list_of_artists(self, artist, admin, client):
        artists = [artist]
        response = client.get(
            '/artists',
            headers=_create_token_auth_header(admin.get_token()))

        assert response.status == '200 OK'
        assert response.get_json() == artists_schema.dump(artists).data

    def test_get_request_returns_first_page_of_artists_by_default(
            self, artists, admin, client):
        response = client.get(
            '/artists',
            headers=_create_token_auth_header(admin.get_token()))

        assert response.status == '200 OK'
        assert response.get_json() == artists_schema.dump(artists[:10]).data

    @pytest.mark.parametrize('page', [1, 2, 3, 4])
    def test_get_request_returns_requested_page_of_artists(
            self, artists, admin, client, page):
        response = client.get(
            '/artists',
            query_string={'page': page},
            headers=_create_token_auth_header(admin.get_token()))

        per_page = 10
        offset = per_page * (page - 1)
        window = artists[offset:offset+per_page]

        assert response.status == '200 OK'
        assert response.get_json() == artists_schema.dump(window).data

    @pytest.mark.parametrize('page', [1, 2, 3, 4])
    @pytest.mark.parametrize('per_page', [1, 2, 5, 10, 20, 50])
    def test_get_request_returns_requested_number_of_artists(
            self, artists, admin, client, page, per_page):
        response = client.get(
            '/artists',
            query_string={'page': page, 'per_page': per_page},
            headers=_create_token_auth_header(admin.get_token()))

        offset = per_page * (page - 1)
        window = artists[offset:offset+per_page]

        assert response.status == '200 OK'
        assert response.get_json() == artists_schema.dump(window).data

    def test_get_request_for_artists_fails_without_authentication(
            self, artists, client):
        response = client.get('/artists')
        assert response.status == '401 UNAUTHORIZED'

    def test_get_request_for_artists_fails_without_admin_status(
            self, artists, user, client):
        response = client.get(
            '/artists',
            headers=_create_token_auth_header(user.get_token()))
        assert response.status == '401 UNAUTHORIZED'


class TestGetArtist:
    def test_get_request_returns_artist(self, artist, admin, client):
        response = client.get(
            '/artists/{id}'.format(id=artist.id),
            headers=_create_token_auth_header(admin.get_token()))

        assert response.status == '200 OK'
        assert response.get_json() == artist_schema.dump(artist).data

    def test_get_request_fails_without_authentication(self, artist, client):
        response = client.get('/artists/{id}'.format(id=artist.id))
        assert response.status == '401 UNAUTHORIZED'

    def test_get_request_fails_without_admin_status(
            self, artist, user, client):
        response = client.get(
            '/artists/{id}'.format(id=artist.id),
            headers=_create_token_auth_header(user.get_token()))
        assert response.status == '401 UNAUTHORIZED'

    def test_get_request_returns_404(self, artist, admin, client):
        response = client.get(
            '/artists/2',
            headers=_create_token_auth_header(admin.get_token()))

        assert response.status == '404 NOT FOUND'
        assert response.get_json() == {
            'error': 'Not Found',
        }


class TestPostArtist:
    def test_post_request_creates_artist(self, client, admin):
        artist = ArtistFactory.build()
        sent = artist_schema.dump(artist).data
        response = client.post(
            '/artists',
            data=json.dumps(sent),
            content_type='application/json',
            headers=_create_token_auth_header(admin.get_token()))

        assert response.status == '201 CREATED'

        recv = response.get_json()

        assert recv is not None
        assert 'id' in recv

        artist = Artist.query.get(recv['id'])

        assert artist is not None
        assert artist.id == recv['id']
        assert artist.name == recv['name']
        assert artist.name == sent['name']

    def test_post_request_fails_without_authentication(self, artist, client):
        artist = ArtistFactory.build()
        data = artist_schema.dump(artist).data
        response = client.post(
            '/artists',
            data=json.dumps(data),
            content_type='application/json')
        assert response.status == '401 UNAUTHORIZED'

    def test_post_request_fails_without_admin_status(
            self, artist, user, client):
        artist = ArtistFactory.build()
        data = artist_schema.dump(artist).data
        response = client.post(
            '/artists',
            data=json.dumps(data),
            content_type='application/json',
            headers=_create_token_auth_header(user.get_token()))
        assert response.status == '401 UNAUTHORIZED'

    def test_post_request_fails_if_name_exists(self, artist, admin, client):
        existing_artist = artist
        artist = ArtistFactory.build(name=existing_artist.name)
        data = artist_schema.dump(artist).data
        response = client.post(
            '/artists',
            data=json.dumps(data),
            content_type='application/json',
            headers=_create_token_auth_header(admin.get_token()))
        assert response.status == '400 BAD REQUEST'
        assert 'name' in response.get_json()['details']

    def test_post_request_fails_if_name_is_invalid(self, admin, client):
        artist = ArtistFactory.build(name='')
        data = artist_schema.dump(artist).data
        response = client.post(
            '/artists',
            data=json.dumps(data),
            content_type='application/json',
            headers=_create_token_auth_header(admin.get_token()))
        assert response.status == '422 UNPROCESSABLE ENTITY'
        assert 'name' in response.get_json()['details']


class TestPutArtist:
    def test_put_request_modifies_name(
            self, client, artist, admin):
        original = artist_schema.dump(artist).data
        data = {'name': 'john'}
        response = client.put(
            '/artists/{id}'.format(id=artist.id),
            data=json.dumps(data),
            content_type='application/json',
            headers=_create_token_auth_header(admin.get_token()))

        assert response.status == '200 OK'
        assert artist.id == original['id']
        assert artist.name == data['name']

    def test_put_request_does_not_modify_id(
            self, client, artist, admin):
        original = artist_schema.dump(artist).data
        data = {'id': 123}
        response = client.put(
            '/artists/{id}'.format(id=artist.id),
            data=json.dumps(data),
            content_type='application/json',
            headers=_create_token_auth_header(admin.get_token()))

        assert response.status == '200 OK'
        assert artist.id == original['id']
        assert artist.name == original['name']

    def test_put_request_returns_modified_artist(self, artist, admin, client):
        original_id = artist.id
        response = client.put(
            '/artists/{id}'.format(id=artist.id),
            data=json.dumps({'name': 'john'}),
            content_type='application/json',
            headers=_create_token_auth_header(admin.get_token()))
        data = response.get_json()
        artist = Artist.query.get(data['id'])

        assert data['id'] == original_id
        assert data['name'] == artist.name

    def test_put_request_fails_without_authentication(self, artist, client):
        response = client.put(
            '/artists/{id}'.format(id=artist.id),
            data=json.dumps({'name': 'john'}),
            content_type='application/json')
        assert response.status == '401 UNAUTHORIZED'

    def test_put_request_fails_without_admin_status(
            self, artist, user, client):
        response = client.put(
            '/artists/{id}'.format(id=artist.id),
            data=json.dumps({'name': 'john'}),
            content_type='application/json',
            headers=_create_token_auth_header(user.get_token()))
        assert response.status == '401 UNAUTHORIZED'

    def test_put_request_fails_if_name_exists(
            self, artists, admin, client):
        artist, artist2 = artists[:2]
        data = {'name': artist2.name}
        response = client.put(
            '/artists/{id}'.format(id=artist.id),
            data=json.dumps(data),
            content_type='application/json',
            headers=_create_token_auth_header(admin.get_token()))
        assert response.status == '400 BAD REQUEST'
        assert 'name' in response.get_json()['details']

    def test_put_request_succeeds_if_name_is_unchanged(
            self, artist, admin, client):
        name = artist.name
        response = client.put(
            '/artists/{id}'.format(id=artist.id),
            data=json.dumps({'name': name}),
            content_type='application/json',
            headers=_create_token_auth_header(admin.get_token()))
        assert response.status == '200 OK'
        assert Artist.query.get(artist.id).name == name

    def test_put_request_fails_if_name_is_invalid(
            self, artist, admin, client):
        response = client.put(
            '/artists/{id}'.format(id=artist.id),
            data=json.dumps({'name': ''}),
            content_type='application/json',
            headers=_create_token_auth_header(admin.get_token()))
        assert response.status == '422 UNPROCESSABLE ENTITY'
        assert 'name' in response.get_json()['details']


class TestDeleteArtist:
    def test_delete_request_removes_artist(self, artist, admin, client):
        response = client.delete(
            '/artists/{id}'.format(id=artist.id),
            headers=_create_token_auth_header(admin.get_token()))

        assert response.status == '204 NO CONTENT'
        assert response.data == b''
        assert Artist.query.get(artist.id) is None

    def test_delete_request_fails_without_authentication(self, artist, client):
        response = client.delete(
            '/artists/{id}'.format(id=artist.id))
        assert response.status == '401 UNAUTHORIZED'

    def test_delete_request_fails_without_admin_status(
            self, artist, user, client):
        response = client.delete(
            '/artists/{id}'.format(id=artist.id),
            headers=_create_token_auth_header(user.get_token()))
        assert response.status == '401 UNAUTHORIZED'
