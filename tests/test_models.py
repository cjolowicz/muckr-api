import pytest

import muckr.extensions
import muckr.models


@pytest.mark.usefixtures('database')
class TestUser:
    def test_create_user(self):
        user = muckr.models.User(
            username='john',
            email='john@example.com',
            password_hash='xxxx')

        assert user.id is None
        assert user.username == 'john'
        assert user.email == 'john@example.com'
        assert user.password_hash == 'xxxx'

        muckr.extensions.database.session.add(user)
        muckr.extensions.database.session.commit()

        assert user.id == 1

    def test_set_password(self):
        user = muckr.models.User(
            username='john',
            email='john@example.com')

        user.set_password('secret')

        assert user.check_password('secret')
        assert not user.check_password('wrong')
