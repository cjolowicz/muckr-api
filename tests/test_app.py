import pytest
import datetime

import muckr.app
import muckr.extensions
import muckr.models


@pytest.fixture
def app():
    app = muckr.app.create_app('tests.config')
    context = app.test_request_context()
    context.push()

    yield app

    context.pop()


@pytest.fixture
def database(app):
    muckr.extensions.database.app = app
    with app.app_context():
        muckr.extensions.database.create_all()

    yield muckr.extensions.database

    muckr.extensions.database.session.close()
    muckr.extensions.database.drop_all()


@pytest.fixture
def client(app, database):
    return app.test_client()


@pytest.mark.usefixtures('database')
class TestPerson:
    def test_person(self):
        birth_date = datetime.datetime(1970, 1, 1)
        person = muckr.models.Person(
            name='john',
            birth_date=birth_date)

        assert person.name == 'john'
        assert person.birth_date == birth_date


class TestViews:
    def test_index(self, client):
        response = client.get('/')
        assert response.data == b'Hello, world!'
