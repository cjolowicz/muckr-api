"""Test user authentication."""
import random

import flask
import pytest

from muckr_api.user.auth import (
    basic_auth_error,
    token_auth_error,
    verify_password,
    verify_token,
)


@pytest.mark.parametrize(
    "username, password, result",
    [
        (None, "example", True),
        ("invalid", "example", False),
        (None, "invalid", False),
        ("invalid", "invalid", False),
    ],
)
def test_verify_password(user, username, password, result):
    if username is None:
        username = user.username
    assert verify_password(username, password) == result
    if username == user.username:
        assert flask.g.current_user.id == user.id
    else:
        assert "current_user" not in flask.g


@pytest.mark.usefixtures("app")
def test_basic_auth_error():
    assert basic_auth_error().status_code == 401
    assert "error" in basic_auth_error().get_json()


def test_verify_token_succeeds_with_valid_token(user):
    token = user.get_token()
    assert verify_token(token)


@pytest.mark.parametrize(
    "token", [None, "", "0" * 64, "".join(random.choices("0123456789abcdef", k=64))]
)
def test_verify_token_fails_with_invalid_token(user, token):
    assert not verify_token(token)
    user.get_token()
    assert not verify_token(token)


@pytest.mark.usefixtures("app")
def test_token_auth_error():
    assert token_auth_error().status_code == 401
    assert "error" in token_auth_error().get_json()
