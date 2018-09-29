import pytest
import yaml

import muckr_service


@pytest.fixture
def client():
    return muckr_service.app.test_client()

def test_person(client):
    response = client.get('/api/person')
    assert yaml.load(response.data) == {
        'num_results': 0,
        'objects': [],
        'page': 1,
        'total_pages': 0
    }
