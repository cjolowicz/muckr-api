"""Factories to help in artist tests."""
from factory import Sequence, SubFactory

from muckr.artist.models import Artist
from tests.factories import BaseFactory
from tests.user.factories import UserFactory


class ArtistFactory(BaseFactory):
    """Artist factory."""

    name = Sequence(lambda n: "artist{0}".format(n))
    user = SubFactory(UserFactory)

    class Meta:
        """Factory configuration."""

        model = Artist
