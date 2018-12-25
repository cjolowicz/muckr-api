"""Test artist models."""
from muckr.artist.models import Artist
from muckr.user.models import User
from tests.artist.factories import ArtistFactory


class TestArtist:
    def test_artist_is_created(self):
        artist = ArtistFactory.build(name="john")

        assert artist.id is None
        assert artist.name == "john"
        assert artist.user.id is None
        assert str(artist) == "<Artist john>"

    def test_artist_is_saved_to_database(self, artist):
        dbartist = Artist.query.get(artist.id)
        assert dbartist.name == artist.name

    def test_artist_has_user(self, artist):
        user = User.query.get(artist.user.id)
        assert user.id == artist.user.id
        assert user.username == artist.user.username
