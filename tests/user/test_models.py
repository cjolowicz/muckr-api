'''Test user models.'''
from datetime import datetime, timedelta

from muckr.user.models import User

from tests.user.factories import UserFactory


class TestUser:
    def test_user_is_created(self):
        user = UserFactory.build(username='john', email='john@example.com')

        assert user.id is None
        assert user.username == 'john'
        assert user.email == 'john@example.com'
        assert user.check_password('example')
        assert user.token is None
        assert user.token_expiration is None
        assert str(user) == '<User john>'

    def test_user_is_saved_to_database(self, user):
        dbuser = User.query.get(user.id)

        assert dbuser.username == user.username
        assert dbuser.email == user.email
        assert dbuser.password_hash == user.password_hash

    def test_set_password_modifies_password(self, user):
        user.set_password('secret')

        assert user.check_password('secret')
        assert not user.check_password('wrong')

    def test_get_token_returns_valid_token(self, user):
        token = user.get_token()
        assert user.token == token
        assert user.token_expiration < datetime.utcnow() + timedelta(3600)
        assert len(token) == 64
        assert all(char in '0123456789abcdef' for char in token)

    def test_revoke_token_expires_token(self, user):
        token = user.get_token()
        user.revoke_token()
        assert user.token == token
        assert user.token_expiration < datetime.utcnow()

    def test_revoke_token_is_noop_without_token(self, user):
        user.revoke_token()
        assert user.token is None
        assert user.token_expiration is None
