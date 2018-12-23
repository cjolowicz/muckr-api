'''Factories to help in artist tests.'''
from factory import Sequence

from muckr.artist.models import Artist
from tests.factories import BaseFactory


class ArtistFactory(BaseFactory):
    '''Artist factory.'''

    name = Sequence(lambda n: 'artist{0}'.format(n))

    class Meta:
        '''Factory configuration.'''

        model = Artist
