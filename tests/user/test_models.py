'''Test user models.'''
from tests.user.factories import UserFactory


class TestUser:
    def test_create_user(self, database):
        user = UserFactory(username='john', email='john@example.com')

        assert user.id is None
        assert user.username == 'john'
        assert user.email == 'john@example.com'
        assert user.check_password('example')
        assert str(user) == '<User john>'

        database.session.commit()

        assert user.id == 1

    def test_set_password(self, user):
        user.set_password('secret')

        assert user.check_password('secret')
        assert not user.check_password('wrong')
