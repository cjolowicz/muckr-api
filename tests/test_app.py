import muckr_service

import pytest


@pytest.fixture
def client():
    return muckr_service.app.test_client()

def test_hello(client):
    response = client.get('/')
    assert response.data == b'Hello, world!'
