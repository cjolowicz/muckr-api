"""Base Factory to help in model tests."""
from factory.alchemy import SQLAlchemyModelFactory

from muckr.extensions import database


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = database.session
