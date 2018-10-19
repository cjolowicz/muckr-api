'''Factories to help in user tests.'''
from datetime import datetime, timedelta
import secrets

from factory import PostGenerationMethodCall, Sequence, LazyFunction
from factory.alchemy import SQLAlchemyModelFactory

from muckr.extensions import database
from muckr.user.models import User


class BaseFactory(SQLAlchemyModelFactory):
    '''Base factory.'''

    class Meta:
        '''Factory configuration.'''

        abstract = True
        sqlalchemy_session = database.session


class UserFactory(BaseFactory):
    '''User factory.'''

    username = Sequence(lambda n: 'user{0}'.format(n))
    email = Sequence(lambda n: 'user{0}@example.com'.format(n))
    password_hash = PostGenerationMethodCall('set_password', 'example')
    token = LazyFunction(lambda: secrets.token_hex(32))
    token_expiration = LazyFunction(
        lambda: datetime.utcnow() + timedelta(seconds=3600))

    class Meta:
        '''Factory configuration.'''

        model = User
