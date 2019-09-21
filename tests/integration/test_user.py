import pytest

USER_JANE = {"username": "jane", "password": "secret", "email": "jane@example.com"}
USER_JOHN = {"username": "john", "password": "secret", "email": "john@example.com"}


@pytest.mark.integration_test
def test_admin_can_create_get_update_delete_list_users(api, admin):
    api.authenticate(admin["username"], admin["password"])

    user = api.users.create(USER_JANE)
    assert user["username"] == USER_JANE["username"]

    user = api.users.get(user["id"])
    assert user["username"] == USER_JANE["username"]
    assert user in api.users.list()

    user = api.users.update(user["id"], USER_JOHN)
    assert user["username"] == USER_JOHN["username"]

    api.users.delete(user["id"])
    user, = api.users.list()
    assert user["username"] == admin["username"]


@pytest.mark.integration_test
def test_user_can_delete_own_account(api):
    user = api.users.create(USER_JANE)
    api.authenticate(USER_JANE["username"], USER_JANE["password"])
    api.users.delete(user["id"])


@pytest.mark.integration_test
def test_admin_can_delete_user(api, admin):
    api.authenticate(admin["username"], admin["password"])
    user = api.users.create(USER_JANE)
    api.users.delete(user["id"])


@pytest.mark.integration_test
def test_admin_can_list_users(api, admin):
    jane = api.users.create(USER_JANE)
    john = api.users.create(USER_JOHN)

    api.authenticate(admin["username"], admin["password"])

    assert {admin["username"], jane["username"], john["username"]} == {
        user["username"] for user in api.users.list()
    }
