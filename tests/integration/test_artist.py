import pytest

USER = {"username": "jane", "password": "secret", "email": "jane@example.com"}


@pytest.mark.integration_test
def test_user_can_create_get_update_delete_list_artists(api):
    api.users.create(USER)
    api.authenticate(USER["username"], USER["password"])

    artist = api.artists.create({"name": "John"})
    assert artist["name"] == "John"

    artist = api.artists.get(artist["id"])
    assert artist["name"] == "John"

    artist, = api.artists.list()
    assert artist["name"] == "John"

    artist = api.artists.update(artist["id"], {"name": "Jane"})
    assert artist["name"] == "Jane"

    api.artists.delete(artist["id"])
    assert not api.artists.list()
