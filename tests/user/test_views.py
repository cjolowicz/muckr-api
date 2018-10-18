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

    def test_get_request_returns_404(self, client):
        response = client.get('/users/1')

        assert response.status == '404 NOT FOUND'
        assert response.get_json() == {
            'error': 'Not Found',
        }

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

    @pytest.mark.parametrize('attribute', ('username', 'email'))
    def test_post_request_fails_if_attribute_exists(
            self, attribute, user, client):
        user, existing_user = UserFactory.build(), user
        data = user_schema.dump(user).data
        data[attribute] = getattr(existing_user, attribute)
        data['password'] = 'secret'
        response = client.post('/users', data=json.dumps(data),
                               content_type='application/json')
        assert response.status == '400 BAD REQUEST'
        assert attribute in response.get_json()['details']

    def test_post_request_fails_if_username_is_empty(
            self, client):
        user = UserFactory.build()
        data = user_schema.dump(user).data
        data['username'] = ''
        data['password'] = 'secret'
        response = client.post('/users', data=json.dumps(data),
                               content_type='application/json')
        assert response.status == '422 UNPROCESSABLE ENTITY'
        assert 'username' in response.get_json()['details']

    @pytest.mark.parametrize('data', [
        {
            'username': 'john',
            'email': 'john@example.com',
            'password': 'new-secret',
        },
        {
            'username': 'john',
        },
        {
            'email': 'john@example.com',
        },
        {
            'password': 'new-secret',
        },
        {
            'id': 123,
        },
    ])
    def test_put_request_modifies_attributes(self, client, user, data):
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

    @pytest.mark.parametrize('attribute', ('username', 'email'))
    def test_put_request_fails_if_attribute_exists(
            self, attribute, users, client):
        user, user2 = users[:2]
        data = {attribute: getattr(user2, attribute)}
        response = client.put('/users/{id}'.format(id=user.id),
                              data=json.dumps(data),
                              content_type='application/json')
        assert response.status == '400 BAD REQUEST'
        assert attribute in response.get_json()['details']

    @pytest.mark.parametrize('attribute', ('username', 'email'))
    def test_put_request_succeeds_if_attribute_is_unchanged(
            self, attribute, user, client):
        value = getattr(user, attribute)
        response = client.put('/users/{id}'.format(id=user.id),
                              data=json.dumps({attribute: value}),
                              content_type='application/json')
        assert response.status == '200 OK'
        assert getattr(User.query.get(user.id), attribute) == value

    @pytest.mark.parametrize('attribute,value', [
        ('username', ''),
        ('email', ''),
        ('email', 'foo'),
    ])
    def test_put_request_fails_if_attribute_is_invalid(
            self, user, client, attribute, value):
        response = client.post('/users', data=json.dumps({'username': ''}),
                               content_type='application/json')
        assert response.status == '422 UNPROCESSABLE ENTITY'
        assert 'username' in response.get_json()['details']

    def test_delete_request_removes_user(self, user, client):
        response = client.delete('/users/{id}'.format(id=user.id))

        assert response.status == '204 NO CONTENT'
        assert response.data == b''
        assert User.query.get(user.id) is None
