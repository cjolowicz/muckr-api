"""Defines fixtures available to user tests."""
import pytest

from tests.user.factories import UserFactory


@pytest.fixture
def user(database):
    user = UserFactory.create()
    database.session.commit()
    return user


@pytest.fixture
def admin(database):
    user = UserFactory.create(username="admin")
    user.is_admin = True
    database.session.commit()
    return user


@pytest.fixture
def users(database):
    users = UserFactory.create_batch(25)  # fill more than 2 pages
    database.session.commit()
    return users
