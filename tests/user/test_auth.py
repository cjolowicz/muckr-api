'''Test user authentication.'''
import flask
import pytest

from muckr.user.auth import verify_password, basic_auth_error


@pytest.mark.parametrize('username, password, result', [
    ('user0', 'example', True),
    ('invalid', 'example', False),
    ('user0', 'invalid', False),
    ('invalid', 'invalid', False),
])
def test_verify_password(user, username, password, result):
    assert verify_password(username, password) == result
    if result:
        assert flask.g.current_user.id == user.id
    else:
        assert 'current_user' not in flask.g


@pytest.mark.usefixtures('app')
def test_basic_auth_error():
    assert basic_auth_error().status_code == 401
    assert 'error' in basic_auth_error().get_json()
