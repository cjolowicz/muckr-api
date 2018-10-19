'''Test user models.'''
from datetime import datetime, timedelta

from tests.user.factories import UserFactory


class TestUser:
    def test_create_user(self, database):
        user = UserFactory(username='john', email='john@example.com')

        assert user.id is None
        assert user.username == 'john'
        assert user.email == 'john@example.com'
        assert user.check_password('example')
        assert user.token is None
        assert user.token_expiration is None
        assert str(user) == '<User john>'

        database.session.commit()

        assert user.id == 1

    def test_set_password(self, user):
        user.set_password('secret')

        assert user.check_password('secret')
        assert not user.check_password('wrong')

    def test_get_token(self, user):
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
