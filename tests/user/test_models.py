"""Test user models."""
import random
from datetime import datetime, timedelta

import pytest

from muckr.user.models import User

from tests.user.factories import UserFactory


def test_user_is_created():
    user = UserFactory.build(username="john", email="john@example.com")

    assert user.id is None
    assert user.username == "john"
    assert user.email == "john@example.com"
    assert user.check_password("example")
    assert user.token is None
    assert user.token_expiration is None
    assert user.is_admin is None
    assert str(user) == "<User john>"


def test_user_is_saved_to_database(user):
    dbuser = User.query.get(user.id)

    assert dbuser.username == user.username
    assert dbuser.email == user.email
    assert dbuser.password_hash == user.password_hash
    assert dbuser.is_admin is False


def test_user_has_artists(user):
    assert user.artists.count() == 0


def test_set_password_modifies_password(user):
    user.set_password("secret")

    assert user.check_password("secret")
    assert not user.check_password("wrong")


def test_get_token_generates_valid_token(user):
    token = user.get_token()
    assert user.token == token
    assert user.token_expiration < datetime.utcnow() + timedelta(3600)
    assert len(token) == 64
    assert all(char in "0123456789abcdef" for char in token)


def test_get_token_returns_existing_token(user):
    token = user.get_token()
    assert user.get_token() == token


def test_revoke_token_expires_token(user):
    token = user.get_token()
    user.revoke_token()
    assert user.token == token
    assert user.token_expiration < datetime.utcnow()


def test_revoke_token_is_noop_without_token(user):
    user.revoke_token()
    assert user.token is None
    assert user.token_expiration is None


def test_check_token_returns_user_if_token_is_valid(user):
    token = user.get_token()
    dbuser = User.check_token(token)
    assert user.id == dbuser.id
    assert user.username == dbuser.username
    assert user.email == dbuser.email


@pytest.mark.parametrize(
    "token", [None, "", "0" * 64, "".join(random.choices("0123456789abcdef", k=64))]
)
def test_check_token_returns_none_if_token_is_invalid(user, token):
    user.get_token()
    assert User.check_token(token) is None


@pytest.mark.parametrize(
    "token", [None, "", "0" * 64, "".join(random.choices("0123456789abcdef", k=64))]
)
def test_check_token_returns_none_if_user_has_no_token(user, token):
    assert User.check_token(token) is None


def test_check_token_returns_none_if_token_is_expired(user):
    token = user.get_token()
    user.revoke_token()
    assert User.check_token(token) is None


def test_check_token_succeeds_for_new_token_after_old_token_was_revoked(user):
    token = user.get_token()
    user.revoke_token()
    token = user.get_token()
    assert User.check_token(token) is not None
