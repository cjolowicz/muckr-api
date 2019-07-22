"""Defines fixtures available to venue tests."""
import pytest

from tests.venue.factories import VenueFactory


@pytest.fixture
def venue(database):
    venue = VenueFactory.create()
    database.session.commit()
    return venue


@pytest.fixture
def venues(database):
    venues = VenueFactory.create_batch(25)  # fill more than 2 pages
    database.session.commit()
    return venues
