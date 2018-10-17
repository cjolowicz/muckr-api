from muckr.user.models import UserSchema

from tests.user.factories import UserFactory


class TestUser:
    def test_get_user(self, database, client):
        user = UserFactory.create()
        database.session.commit()

        response = client.get('/users/{id}'.format(id=user.id))
        data, errors = UserSchema().dump(user)

        assert response.status == '200 OK'
        assert response.get_json() == data
