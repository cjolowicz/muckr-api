import json

from muckr.user.models import User, UserSchema

from tests.user.factories import UserFactory


class TestUser:
    def test_get_user(self, database, client):
        user = UserFactory.create()
        database.session.commit()

        response = client.get('/users/{id}'.format(id=user.id))

        assert response.status == '200 OK'
        assert response.get_json() == UserSchema().dump(user).data

    def test_create_user(self, client):
        user = UserFactory.build()
        data = UserSchema().dump(user).data

        response = client.post('/users', data=json.dumps(data),
                               content_type='application/json')

        data['id'] = response.get_json()['id']

        assert response.status == '201 CREATED'
        assert response.get_json()['id'] > 0
        assert response.get_json() == data

    def test_create_user_with_password(self, client):
        data = {
            'username': 'user0',
            'email': 'user0@example.com',
            'password': 'secret',
        }

        response = client.post('/users', data=json.dumps(data),
                               content_type='application/json')

        user = User.query.get(response.get_json()['id'])

        assert user.check_password(data['password'])
