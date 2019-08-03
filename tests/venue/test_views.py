"""Test venue views."""
import json
import pytest

from muckr.venue.models import Venue
from muckr.venue.views import venue_schema, venues_schema

from tests.venue.factories import VenueFactory
from tests.utils import create_token_auth_header


class TestGetVenues:
    def test_get_request_returns_list_of_venues(self, venue, client):
        response = client.get(
            "/venues", headers=create_token_auth_header(venue.user.get_token())
        )

        assert response.status == "200 OK"
        assert response.get_json() == venues_schema.dump([venue])

    def test_get_request_returns_first_page_of_venues_by_default(
        self, client, user, database
    ):
        venues = VenueFactory.create_batch(25, user=user)
        database.session.commit()
        response = client.get(
            "/venues", headers=create_token_auth_header(user.get_token())
        )

        assert response.status == "200 OK"
        assert response.get_json() == venues_schema.dump(venues[:10])

    @pytest.mark.parametrize("page", [1, 2, 3, 4])
    def test_get_request_returns_requested_page_of_venues(
        self, client, user, database, page
    ):
        venues = VenueFactory.create_batch(25, user=user)
        database.session.commit()
        response = client.get(
            "/venues",
            query_string={"page": page},
            headers=create_token_auth_header(user.get_token()),
        )

        per_page = 10
        offset = per_page * (page - 1)
        window = venues[offset : offset + per_page]

        assert response.status == "200 OK"
        assert response.get_json() == venues_schema.dump(window)

    @pytest.mark.parametrize("page", [1, 2, 3, 4])
    @pytest.mark.parametrize("per_page", [1, 2, 5, 10, 20, 50])
    def test_get_request_returns_requested_number_of_venues(
        self, client, user, database, page, per_page
    ):
        venues = VenueFactory.create_batch(25, user=user)
        database.session.commit()
        response = client.get(
            "/venues",
            query_string={"page": page, "per_page": per_page},
            headers=create_token_auth_header(user.get_token()),
        )

        offset = per_page * (page - 1)
        window = venues[offset : offset + per_page]

        assert response.status == "200 OK"
        assert response.get_json() == venues_schema.dump(window)

    def test_get_request_for_venues_fails_without_authentication(self, client):
        response = client.get("/venues")
        assert response.status == "401 UNAUTHORIZED"


class TestGetVenue:
    def test_get_request_returns_venue(self, venue, client):
        response = client.get(
            "/venues/{id}".format(id=venue.id),
            headers=create_token_auth_header(venue.user.get_token()),
        )

        assert response.status == "200 OK"
        assert response.get_json() == venue_schema.dump(venue)

    def test_get_request_fails_without_authentication(self, venue, client):
        response = client.get("/venues/{id}".format(id=venue.id))
        assert response.status == "401 UNAUTHORIZED"

    def test_get_request_returns_404_if_venue_not_found(self, venue, client):
        response = client.get(
            "/venues/2", headers=create_token_auth_header(venue.user.get_token())
        )

        assert response.status == "404 NOT FOUND"
        assert response.get_json() == {"error": "Not Found"}

    def test_get_request_returns_404_for_venue_of_another_user(self, client, database):
        venue1, venue2 = VenueFactory.create_batch(2)
        database.session.commit()
        response = client.get(
            "/venues/{id}".format(id=venue1.id),
            headers=create_token_auth_header(venue2.user.get_token()),
        )

        assert response.status == "404 NOT FOUND"
        assert response.get_json() == {"error": "Not Found"}

    def test_get_request_succeeds_for_venue_of_another_user_if_admin(
        self, client, venue, admin
    ):
        response = client.get(
            "/venues/{id}".format(id=venue.id),
            headers=create_token_auth_header(admin.get_token()),
        )

        assert response.status == "200 OK"
        assert response.get_json() == venue_schema.dump(venue)


class TestPostVenue:
    def test_post_request_creates_venue(self, client, user):
        venue = VenueFactory.build()
        sent = venue_schema.dump(venue)
        del sent["id"]
        response = client.post(
            "/venues",
            data=json.dumps(sent),
            content_type="application/json",
            headers=create_token_auth_header(user.get_token()),
        )

        assert response.status == "201 CREATED"

        recv = response.get_json()

        assert recv is not None
        assert "id" in recv

        venue = Venue.query.get(recv["id"])

        assert venue is not None
        assert venue.id == recv["id"]
        assert venue.name == recv["name"]
        assert venue.name == sent["name"]
        assert venue.user.id == user.id

    def test_post_request_fails_without_authentication(self, venue, client):
        venue = VenueFactory.build()
        data = venue_schema.dump(venue)
        response = client.post(
            "/venues", data=json.dumps(data), content_type="application/json"
        )
        assert response.status == "401 UNAUTHORIZED"

    def test_post_request_fails_if_name_exists(self, venue, client):
        name, user = venue.name, venue.user
        venue = VenueFactory.build(name=name)
        data = venue_schema.dump(venue)
        del data["id"]
        response = client.post(
            "/venues",
            data=json.dumps(data),
            content_type="application/json",
            headers=create_token_auth_header(user.get_token()),
        )
        assert response.status == "400 BAD REQUEST"
        assert "name" in response.get_json()["details"]

    def test_post_request_fails_if_name_is_invalid(self, user, client):
        venue = VenueFactory.build(name="")
        data = venue_schema.dump(venue)
        response = client.post(
            "/venues",
            data=json.dumps(data),
            content_type="application/json",
            headers=create_token_auth_header(user.get_token()),
        )
        assert response.status == "422 UNPROCESSABLE ENTITY"
        assert "name" in response.get_json()["details"]


class TestPutVenue:
    def test_put_request_modifies_name(self, client, venue):
        original = venue_schema.dump(venue)
        data = {"name": "john"}
        response = client.put(
            "/venues/{id}".format(id=venue.id),
            data=json.dumps(data),
            content_type="application/json",
            headers=create_token_auth_header(venue.user.get_token()),
        )

        assert response.status == "200 OK"
        assert venue.id == original["id"]
        assert venue.name == data["name"]

    def test_put_request_returns_404_for_venue_of_another_user(self, client, database):
        venue1, venue2 = VenueFactory.create_batch(2)
        database.session.commit()
        data = {"name": "john"}
        response = client.put(
            "/venues/{id}".format(id=venue1.id),
            data=json.dumps(data),
            content_type="application/json",
            headers=create_token_auth_header(venue2.user.get_token()),
        )

        assert response.status == "404 NOT FOUND"
        assert response.get_json() == {"error": "Not Found"}

    def test_put_request_succeeds_for_venue_of_another_user_if_admin(
        self, client, venue, admin
    ):
        data = {"name": "john"}
        response = client.put(
            "/venues/{id}".format(id=venue.id),
            data=json.dumps(data),
            content_type="application/json",
            headers=create_token_auth_header(admin.get_token()),
        )

        assert response.status == "200 OK"
        assert response.get_json() == venue_schema.dump(venue)

    def test_put_request_fails_if_id_is_passed(self, client, venue):
        response = client.put(
            "/venues/{id}".format(id=venue.id),
            data=json.dumps({"id": 123}),
            content_type="application/json",
            headers=create_token_auth_header(venue.user.get_token()),
        )

        assert response.status == "422 UNPROCESSABLE ENTITY"
        assert "id" in response.get_json()["details"]

    def test_put_request_returns_modified_venue(self, venue, client):
        original_id = venue.id
        response = client.put(
            "/venues/{id}".format(id=venue.id),
            data=json.dumps({"name": "john"}),
            content_type="application/json",
            headers=create_token_auth_header(venue.user.get_token()),
        )
        data = response.get_json()
        venue = Venue.query.get(data["id"])

        assert data["id"] == original_id
        assert data["name"] == venue.name

    def test_put_request_fails_without_authentication(self, venue, client):
        response = client.put(
            "/venues/{id}".format(id=venue.id),
            data=json.dumps({"name": "john"}),
            content_type="application/json",
        )
        assert response.status == "401 UNAUTHORIZED"

    def test_put_request_fails_if_name_exists(self, client, user, database):
        venue1, venue2 = VenueFactory.create_batch(2, user=user)
        database.session.commit()
        response = client.put(
            "/venues/{id}".format(id=venue1.id),
            data=json.dumps({"name": venue2.name}),
            content_type="application/json",
            headers=create_token_auth_header(user.get_token()),
        )
        assert response.status == "400 BAD REQUEST"
        assert "name" in response.get_json()["details"]

    def test_put_request_succeeds_if_name_exists_for_another_user(
        self, client, database
    ):
        venue1, venue2 = VenueFactory.create_batch(2)
        database.session.commit()
        response = client.put(
            "/venues/{id}".format(id=venue1.id),
            data=json.dumps({"name": venue2.name}),
            content_type="application/json",
            headers=create_token_auth_header(venue1.user.get_token()),
        )
        assert response.status == "200 OK"
        assert Venue.query.get(venue1.id).name == venue2.name

    def test_put_request_succeeds_if_name_is_unchanged(self, venue, client):
        name = venue.name
        response = client.put(
            "/venues/{id}".format(id=venue.id),
            data=json.dumps({"name": name}),
            content_type="application/json",
            headers=create_token_auth_header(venue.user.get_token()),
        )
        assert response.status == "200 OK"
        assert Venue.query.get(venue.id).name == name

    def test_put_request_fails_if_name_is_invalid(self, venue, client):
        response = client.put(
            "/venues/{id}".format(id=venue.id),
            data=json.dumps({"name": ""}),
            content_type="application/json",
            headers=create_token_auth_header(venue.user.get_token()),
        )
        assert response.status == "422 UNPROCESSABLE ENTITY"
        assert "name" in response.get_json()["details"]


class TestDeleteVenue:
    def test_delete_request_removes_venue(self, venue, client):
        response = client.delete(
            "/venues/{id}".format(id=venue.id),
            headers=create_token_auth_header(venue.user.get_token()),
        )

        assert response.status == "204 NO CONTENT"
        assert response.data == b""
        assert Venue.query.get(venue.id) is None

    def test_delete_request_returns_404_if_venue_not_found(self, venue, client):
        response = client.delete(
            "/venues/2", headers=create_token_auth_header(venue.user.get_token())
        )

        assert response.status == "404 NOT FOUND"
        assert response.get_json() == {"error": "Not Found"}

    def test_delete_request_returns_404_for_venue_of_another_user(
        self, client, database
    ):
        venue1, venue2 = VenueFactory.create_batch(2)
        database.session.commit()
        response = client.delete(
            "/venues/{id}".format(id=venue1.id),
            headers=create_token_auth_header(venue2.user.get_token()),
        )

        assert response.status == "404 NOT FOUND"
        assert response.get_json() == {"error": "Not Found"}

    def test_delete_request_succeeds_for_venue_of_another_user_if_admin(
        self, client, venue, admin, database
    ):
        response = client.delete(
            "/venues/{id}".format(id=venue.id),
            headers=create_token_auth_header(admin.get_token()),
        )

        assert response.status == "204 NO CONTENT"
        assert response.data == b""
        assert Venue.query.get(venue.id) is None

    def test_delete_request_fails_without_authentication(self, venue, client):
        response = client.delete("/venues/{id}".format(id=venue.id))
        assert response.status == "401 UNAUTHORIZED"
