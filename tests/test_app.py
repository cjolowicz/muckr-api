import os

import environs
import pytest

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
class TestModels:
    def test_user(self):
        user = muckr.models.User(
            username='john',
            email='john@example.com',
            password_hash='xxxx')

        assert user.id is None
        assert user.username == 'john'
        assert user.email == 'john@example.com'
        assert user.password_hash == 'xxxx'

        muckr.extensions.database.session.add(user)
        muckr.extensions.database.session.commit()

        assert user.id == 1


class TestViews:
    def test_index(self, client):
        response = client.get('/')
        assert response.data == b'Hello, world!'


@pytest.mark.usefixtures('app')
class TestConfig:
    def test_config_requires_secret_key(self):
        try:
            del os.environ['SECRET_KEY']
        except KeyError:
            pass

        env = environs.Env()
        env.read_env()

        if 'SECRET_KEY' in os.environ:
            pytest.skip('SECRET_KEY set in .env file')

        with pytest.raises(environs.EnvError):
            import muckr.config # noqa

    def test_config_reads_environment_variables(self):
        os.environ['SECRET_KEY'] = 'secret-key'
        os.environ['DATABASE_URL'] = 'sqlite://'

        import muckr.config
        assert muckr.config.SECRET_KEY == 'secret-key'
        assert muckr.config.SQLALCHEMY_DATABASE_URI == 'sqlite://'
