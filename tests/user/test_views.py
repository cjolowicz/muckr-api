import pytest
import json

from muckr.user.models import User
from muckr.user.views import user_schema, users_schema

from tests.user.factories import UserFactory


@pytest.fixture
def user(database):
    user = UserFactory.create()
    database.session.commit()
    return user


@pytest.fixture
def users(database):
    users = UserFactory.create_batch(10)
    database.session.commit()
    return users


class TestUser:
    def test_get_request_returns_list_of_users(self, users, client):
        response = client.get('/users')

        assert response.status == '200 OK'
        assert response.get_json() == users_schema.dump(users).data

    def test_get_request_returns_user(self, user, client):
        response = client.get('/users/{id}'.format(id=user.id))

        assert response.status == '200 OK'
        assert response.get_json() == user_schema.dump(user).data

    def test_post_request_creates_user(self, client):
        user = UserFactory.build()
        sent = user_schema.dump(user).data
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

    def check_attributes_after_put_request(self, client, user, data):
        original = user_schema.dump(user).data
        original['password'] = 'example'
        response = client.put('/users/{id}'.format(id=user.id),
                              data=json.dumps(data),
                              content_type='application/json')

        assert response.status == '200 OK'

        for key in ['id', 'username', 'email', 'password']:
            value = data[key] if key in data and key != 'id' else original[key]
            if key == 'password':
                assert user.check_password(value)
            else:
                assert getattr(user, key) == value

    def test_put_request_modifies_username_and_email(self, user, client):
        self.check_attributes_after_put_request(client, user, {
            'username': 'john',
            'email': 'john@example.com',
        })

    def test_put_request_modifies_password(self, user, client):
        self.check_attributes_after_put_request(client, user, {
            'password': 'new-secret'
        })

    def test_put_request_does_not_modify_id(self, user, client):
        self.check_attributes_after_put_request(client, user, {
            'id': 123,
        })

    def test_put_request_returns_modified_user(self, user, client):
        original_id = user.id
        response = client.put('/users/{id}'.format(id=user.id),
                              data=json.dumps({'email': 'john@example.com'}),
                              content_type='application/json')
        data = response.get_json()
        user = User.query.get(data['id'])

        assert data['id'] == original_id
        for key in ['username', 'email']:
            assert data[key] == getattr(user, key)
        assert 'password' not in data

    def test_delete_request_removes_user(self, user, client):
        response = client.delete('/users/{id}'.format(id=user.id))

        assert response.status == '204 NO CONTENT'
        assert response.data == b''
        assert User.query.get(user.id) is None
