"""Factories to help in venue tests."""
from factory import Sequence, SubFactory

from muckr_api.venue.models import Venue
from tests.factories import BaseFactory
from tests.user.factories import UserFactory


class VenueFactory(BaseFactory):
    """Venue factory."""

    name = Sequence(lambda n: "venue{0}".format(n))
    city = Sequence(lambda n: "city{0}".format(n))
    country = Sequence(lambda n: "country{0}".format(n))
    user = SubFactory(UserFactory)

    class Meta:
        """Factory configuration."""

        model = Venue
