'''Test main views.'''


class TestViews:
    def test_index(self, client):
        response = client.get('/')
        assert response.data == b'Hello, world!'
