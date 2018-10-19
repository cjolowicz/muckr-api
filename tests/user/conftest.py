'''Defines fixtures available to user tests.'''
import pytest

from tests.user.factories import UserFactory


@pytest.fixture
def user(database):
    user = UserFactory.create()
    database.session.commit()
    return user


@pytest.fixture
def users(database):
    users = UserFactory.create_batch(10)
    database.session.commit()
    return users
