"""Defines fixtures available to all tests."""
import pytest

import muckr_api.app
import muckr_api.extensions


@pytest.fixture
def app():
    app = muckr_api.app.create_app("tests.config")
    context = app.test_request_context()
    context.push()

    yield app

    context.pop()


@pytest.fixture
def database(app):
    muckr_api.extensions.database.app = app
    with app.app_context():
        muckr_api.extensions.database.create_all()

    yield muckr_api.extensions.database

    muckr_api.extensions.database.session.close()
    muckr_api.extensions.database.drop_all()


@pytest.fixture
def client(app, database):
    return app.test_client()
