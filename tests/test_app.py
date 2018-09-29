import pytest
import json

import muckr_service


@pytest.fixture
def client():
    return muckr_service.app.test_client()

def test_person(client):
    response = client.get('/api/person')
    assert json.loads(response.data) == {
        'num_results': 0,
        'objects': [],
        'page': 1,
        'total_pages': 0
    }
