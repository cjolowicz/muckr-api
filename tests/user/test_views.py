from muckr.user.models import UserSchema

import tests.user.factories


class TestUser:
    def test_get_user(self, database, client):
        user = tests.user.factories.UserFactory.create()
        database.session.commit()

        response = client.get('/users/{id}'.format(id=user.id))
        data, errors = UserSchema().dumps(user)

        assert response.data.decode('utf-8') == data
