'''Test main views.'''
import muckr


class TestViews:
    def test_index(self, client):
        response = client.get('/')
        assert muckr.__version__ in response.data.decode('utf-8')
