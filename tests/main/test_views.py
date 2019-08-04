"""Test main views."""
import muckr_api


class TestViews:
    def test_index(self, client):
        response = client.get("/")
        assert muckr_api.__version__ in response.data.decode("utf-8")
