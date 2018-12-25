"""Test artist views."""
import json
import pytest

from muckr.artist.models import Artist
from muckr.artist.views import artist_schema, artists_schema

from tests.artist.factories import ArtistFactory
from tests.utils import create_token_auth_header


class TestGetArtists:
    def test_get_request_returns_list_of_artists(self, artist, client):
        response = client.get(
            "/artists", headers=create_token_auth_header(artist.user.get_token())
        )

        assert response.status == "200 OK"
        assert response.get_json() == artists_schema.dump([artist])

    def test_get_request_returns_first_page_of_artists_by_default(
        self, client, user, database
    ):
        artists = ArtistFactory.create_batch(25, user=user)
        database.session.commit()
        response = client.get(
            "/artists", headers=create_token_auth_header(user.get_token())
        )

        assert response.status == "200 OK"
        assert response.get_json() == artists_schema.dump(artists[:10])

    @pytest.mark.parametrize("page", [1, 2, 3, 4])
    def test_get_request_returns_requested_page_of_artists(
        self, client, user, database, page
    ):
        artists = ArtistFactory.create_batch(25, user=user)
        database.session.commit()
        response = client.get(
            "/artists",
            query_string={"page": page},
            headers=create_token_auth_header(user.get_token()),
        )

        per_page = 10
        offset = per_page * (page - 1)
        window = artists[offset : offset + per_page]

        assert response.status == "200 OK"
        assert response.get_json() == artists_schema.dump(window)

    @pytest.mark.parametrize("page", [1, 2, 3, 4])
    @pytest.mark.parametrize("per_page", [1, 2, 5, 10, 20, 50])
    def test_get_request_returns_requested_number_of_artists(
        self, client, user, database, page, per_page
    ):
        artists = ArtistFactory.create_batch(25, user=user)
        database.session.commit()
        response = client.get(
            "/artists",
            query_string={"page": page, "per_page": per_page},
            headers=create_token_auth_header(user.get_token()),
        )

        offset = per_page * (page - 1)
        window = artists[offset : offset + per_page]

        assert response.status == "200 OK"
        assert response.get_json() == artists_schema.dump(window)

    def test_get_request_for_artists_fails_without_authentication(self, client):
        response = client.get("/artists")
        assert response.status == "401 UNAUTHORIZED"


class TestGetArtist:
    def test_get_request_returns_artist(self, artist, client):
        response = client.get(
            "/artists/{id}".format(id=artist.id),
            headers=create_token_auth_header(artist.user.get_token()),
        )

        assert response.status == "200 OK"
        assert response.get_json() == artist_schema.dump(artist)

    def test_get_request_fails_without_authentication(self, artist, client):
        response = client.get("/artists/{id}".format(id=artist.id))
        assert response.status == "401 UNAUTHORIZED"

    def test_get_request_returns_404_if_artist_not_found(self, artist, client):
        response = client.get(
            "/artists/2", headers=create_token_auth_header(artist.user.get_token())
        )

        assert response.status == "404 NOT FOUND"
        assert response.get_json() == {"error": "Not Found"}

    def test_get_request_returns_404_for_artist_of_another_user(self, client, database):
        artist1, artist2 = ArtistFactory.create_batch(2)
        database.session.commit()
        response = client.get(
            "/artists/{id}".format(id=artist1.id),
            headers=create_token_auth_header(artist2.user.get_token()),
        )

        assert response.status == "404 NOT FOUND"
        assert response.get_json() == {"error": "Not Found"}

    def test_get_request_succeeds_for_artist_of_another_user_if_admin(
        self, client, artist, admin
    ):
        response = client.get(
            "/artists/{id}".format(id=artist.id),
            headers=create_token_auth_header(admin.get_token()),
        )

        assert response.status == "200 OK"
        assert response.get_json() == artist_schema.dump(artist)


class TestPostArtist:
    def test_post_request_creates_artist(self, client, user):
        artist = ArtistFactory.build()
        sent = artist_schema.dump(artist)
        del sent["id"]
        response = client.post(
            "/artists",
            data=json.dumps(sent),
            content_type="application/json",
            headers=create_token_auth_header(user.get_token()),
        )

        assert response.status == "201 CREATED"

        recv = response.get_json()

        assert recv is not None
        assert "id" in recv

        artist = Artist.query.get(recv["id"])

        assert artist is not None
        assert artist.id == recv["id"]
        assert artist.name == recv["name"]
        assert artist.name == sent["name"]
        assert artist.user.id == user.id

    def test_post_request_fails_without_authentication(self, artist, client):
        artist = ArtistFactory.build()
        data = artist_schema.dump(artist)
        response = client.post(
            "/artists", data=json.dumps(data), content_type="application/json"
        )
        assert response.status == "401 UNAUTHORIZED"

    def test_post_request_fails_if_name_exists(self, artist, client):
        name, user = artist.name, artist.user
        artist = ArtistFactory.build(name=name)
        data = artist_schema.dump(artist)
        del data["id"]
        response = client.post(
            "/artists",
            data=json.dumps(data),
            content_type="application/json",
            headers=create_token_auth_header(user.get_token()),
        )
        assert response.status == "400 BAD REQUEST"
        assert "name" in response.get_json()["details"]

    def test_post_request_fails_if_name_is_invalid(self, user, client):
        artist = ArtistFactory.build(name="")
        data = artist_schema.dump(artist)
        response = client.post(
            "/artists",
            data=json.dumps(data),
            content_type="application/json",
            headers=create_token_auth_header(user.get_token()),
        )
        assert response.status == "422 UNPROCESSABLE ENTITY"
        assert "name" in response.get_json()["details"]


class TestPutArtist:
    def test_put_request_modifies_name(self, client, artist):
        original = artist_schema.dump(artist)
        data = {"name": "john"}
        response = client.put(
            "/artists/{id}".format(id=artist.id),
            data=json.dumps(data),
            content_type="application/json",
            headers=create_token_auth_header(artist.user.get_token()),
        )

        assert response.status == "200 OK"
        assert artist.id == original["id"]
        assert artist.name == data["name"]

    def test_put_request_returns_404_for_artist_of_another_user(self, client, database):
        artist1, artist2 = ArtistFactory.create_batch(2)
        database.session.commit()
        data = {"name": "john"}
        response = client.put(
            "/artists/{id}".format(id=artist1.id),
            data=json.dumps(data),
            content_type="application/json",
            headers=create_token_auth_header(artist2.user.get_token()),
        )

        assert response.status == "404 NOT FOUND"
        assert response.get_json() == {"error": "Not Found"}

    def test_put_request_succeeds_for_artist_of_another_user_if_admin(
        self, client, artist, admin
    ):
        data = {"name": "john"}
        response = client.put(
            "/artists/{id}".format(id=artist.id),
            data=json.dumps(data),
            content_type="application/json",
            headers=create_token_auth_header(admin.get_token()),
        )

        assert response.status == "200 OK"
        assert response.get_json() == artist_schema.dump(artist)

    def test_put_request_fails_if_id_is_passed(self, client, artist):
        response = client.put(
            "/artists/{id}".format(id=artist.id),
            data=json.dumps({"id": 123}),
            content_type="application/json",
            headers=create_token_auth_header(artist.user.get_token()),
        )

        assert response.status == "422 UNPROCESSABLE ENTITY"
        assert "id" in response.get_json()["details"]

    def test_put_request_returns_modified_artist(self, artist, client):
        original_id = artist.id
        response = client.put(
            "/artists/{id}".format(id=artist.id),
            data=json.dumps({"name": "john"}),
            content_type="application/json",
            headers=create_token_auth_header(artist.user.get_token()),
        )
        data = response.get_json()
        artist = Artist.query.get(data["id"])

        assert data["id"] == original_id
        assert data["name"] == artist.name

    def test_put_request_fails_without_authentication(self, artist, client):
        response = client.put(
            "/artists/{id}".format(id=artist.id),
            data=json.dumps({"name": "john"}),
            content_type="application/json",
        )
        assert response.status == "401 UNAUTHORIZED"

    def test_put_request_fails_if_name_exists(self, client, user, database):
        artist1, artist2 = ArtistFactory.create_batch(2, user=user)
        database.session.commit()
        response = client.put(
            "/artists/{id}".format(id=artist1.id),
            data=json.dumps({"name": artist2.name}),
            content_type="application/json",
            headers=create_token_auth_header(user.get_token()),
        )
        assert response.status == "400 BAD REQUEST"
        assert "name" in response.get_json()["details"]

    def test_put_request_succeeds_if_name_exists_for_another_user(
        self, client, database
    ):
        artist1, artist2 = ArtistFactory.create_batch(2)
        database.session.commit()
        response = client.put(
            "/artists/{id}".format(id=artist1.id),
            data=json.dumps({"name": artist2.name}),
            content_type="application/json",
            headers=create_token_auth_header(artist1.user.get_token()),
        )
        assert response.status == "200 OK"
        assert Artist.query.get(artist1.id).name == artist2.name

    def test_put_request_succeeds_if_name_is_unchanged(self, artist, client):
        name = artist.name
        response = client.put(
            "/artists/{id}".format(id=artist.id),
            data=json.dumps({"name": name}),
            content_type="application/json",
            headers=create_token_auth_header(artist.user.get_token()),
        )
        assert response.status == "200 OK"
        assert Artist.query.get(artist.id).name == name

    def test_put_request_fails_if_name_is_invalid(self, artist, client):
        response = client.put(
            "/artists/{id}".format(id=artist.id),
            data=json.dumps({"name": ""}),
            content_type="application/json",
            headers=create_token_auth_header(artist.user.get_token()),
        )
        assert response.status == "422 UNPROCESSABLE ENTITY"
        assert "name" in response.get_json()["details"]


class TestDeleteArtist:
    def test_delete_request_removes_artist(self, artist, client):
        response = client.delete(
            "/artists/{id}".format(id=artist.id),
            headers=create_token_auth_header(artist.user.get_token()),
        )

        assert response.status == "204 NO CONTENT"
        assert response.data == b""
        assert Artist.query.get(artist.id) is None

    def test_delete_request_returns_404_if_artist_not_found(self, artist, client):
        response = client.delete(
            "/artists/2", headers=create_token_auth_header(artist.user.get_token())
        )

        assert response.status == "404 NOT FOUND"
        assert response.get_json() == {"error": "Not Found"}

    def test_delete_request_returns_404_for_artist_of_another_user(
        self, client, database
    ):
        artist1, artist2 = ArtistFactory.create_batch(2)
        database.session.commit()
        response = client.delete(
            "/artists/{id}".format(id=artist1.id),
            headers=create_token_auth_header(artist2.user.get_token()),
        )

        assert response.status == "404 NOT FOUND"
        assert response.get_json() == {"error": "Not Found"}

    def test_delete_request_succeeds_for_artist_of_another_user_if_admin(
        self, client, artist, admin, database
    ):
        response = client.delete(
            "/artists/{id}".format(id=artist.id),
            headers=create_token_auth_header(admin.get_token()),
        )

        assert response.status == "204 NO CONTENT"
        assert response.data == b""
        assert Artist.query.get(artist.id) is None

    def test_delete_request_fails_without_authentication(self, artist, client):
        response = client.delete("/artists/{id}".format(id=artist.id))
        assert response.status == "401 UNAUTHORIZED"
