from muckr.user.models import UserSchema

import tests.user.factories


class TestUser:
    def test_get_user(self, database, client):
        user = tests.user.factories.UserFactory.create()
        database.session.commit()

        response = client.get('/users/{id}'.format(id=user.id))
        data, errors = UserSchema().dump(user)

        assert response.status == '200 OK'
        assert response.get_json() == data
