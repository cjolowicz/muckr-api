'''Test user authentication.'''
import pytest

from muckr.user.auth import verify_password, basic_auth_error

from tests.user.factories import UserFactory


@pytest.mark.parametrize('username, password, result', [
    ('user0', 'example', True),
    ('invalid', 'example', False),
    ('user0', 'invalid', False),
    ('invalid', 'invalid', False),
])
def test_verify_password(database, username, password, result):
    UserFactory.create()
    database.session.commit()

    assert verify_password(username, password) == result


@pytest.mark.usefixtures('app')
def test_basic_auth_error():
    assert basic_auth_error().status_code == 401
    assert 'error' in basic_auth_error().get_json()
