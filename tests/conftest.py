'''Defines fixtures available to all tests.'''
import pytest

import muckr.app
import muckr.extensions


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
