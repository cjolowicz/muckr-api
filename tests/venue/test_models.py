"""Test venue models."""
from muckr.venue.models import Venue
from muckr.user.models import User
from tests.venue.factories import VenueFactory


class TestVenue:
    def test_venue_is_created(self):
        venue = VenueFactory.build(name="club")

        assert venue.id is None
        assert venue.name == "club"
        assert venue.user.id is None
        assert str(venue) == "<Venue club>"

    def test_venue_is_saved_to_database(self, venue):
        dbvenue = Venue.query.get(venue.id)
        assert dbvenue.name == venue.name

    def test_venue_has_user(self, venue):
        user = User.query.get(venue.user.id)
        assert user.id == venue.user.id
        assert user.username == venue.user.username
