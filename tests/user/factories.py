"""Factories to help in user tests."""
from factory import PostGenerationMethodCall, Sequence

from muckr_api.user.models import User
from tests.factories import BaseFactory


class UserFactory(BaseFactory):
    """User factory."""

    username = Sequence(lambda n: "user{0}".format(n))
    email = Sequence(lambda n: "user{0}@example.com".format(n))
    password_hash = PostGenerationMethodCall("set_password", "example")

    class Meta:
        """Factory configuration."""

        model = User
