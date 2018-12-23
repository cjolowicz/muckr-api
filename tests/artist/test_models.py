'''Test artist models.'''
from muckr.artist.models import Artist
from tests.artist.factories import ArtistFactory


class TestArtist:
    def test_artist_is_created(self):
        artist = ArtistFactory.build(name='john')

        assert artist.id is None
        assert artist.name == 'john'
        assert str(artist) == '<Artist john>'

    def test_artist_is_saved_to_database(self, artist):
        dbartist = Artist.query.get(artist.id)

        assert dbartist.name == artist.name
