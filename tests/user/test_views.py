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
        sent = UserSchema().dump(user).data
        sent['password'] = 'secret'

        response = client.post('/users', data=json.dumps(sent),
                               content_type='application/json')

        assert response.status == '201 CREATED'

        recv = response.get_json()

        assert recv is not None
        assert 'id' in recv

        user = User.query.get(recv['id'])

        assert user is not None
        assert user.id == recv['id']
        for key in ['username', 'email']:
            assert sent[key] == recv[key]
            assert sent[key] == getattr(user, key)
        assert 'password' not in recv
        assert user.check_password(sent['password'])
