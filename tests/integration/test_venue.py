import pytest

USER = {"username": "jane", "password": "secret", "email": "jane@example.com"}


@pytest.mark.integration_test
def test_user_can_create_get_update_delete_list_venues(api):
    api.users.create(USER)
    api.authenticate(USER["username"], USER["password"])

    venue = api.venues.create({"name": "Lido", "city": "Berlin", "country": "Germany"})
    assert venue["name"] == "Lido"

    venue = api.venues.get(venue["id"])
    assert venue["name"] == "Lido"

    venue, = api.venues.list()
    assert venue["name"] == "Lido"

    venue = api.venues.update(venue["id"], {"name": "Festsaal"})
    assert venue["name"] == "Festsaal"

    api.venues.delete(venue["id"])
    assert not api.venues.list()
