'''Defines fixtures available to artist tests.'''
import pytest

from tests.artist.factories import ArtistFactory


@pytest.fixture
def artist(database):
    artist = ArtistFactory.create()
    database.session.commit()
    return artist


@pytest.fixture
def artists(database):
    artists = ArtistFactory.create_batch(25)  # fill more than 2 pages
    database.session.commit()
    return artists
