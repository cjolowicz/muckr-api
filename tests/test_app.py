import pytest
import json

import muckr_service

@pytest.fixture
def app():
    return muckr_service.create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite://', # in-memory database
    })

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_person(client):
    response = client.get('/api/person')
    assert json.loads(response.data) == {
        'num_results': 0,
        'objects': [],
        'page': 1,
        'total_pages': 0
    }

def test_post_person(client):
    person = {
        'name': u'Abraham Lincoln',
        'birth_date': u'1809-02-12',
    }

    response = client.post(
        '/api/person',
        data=json.dumps(person),
        headers={'Content-Type': 'application/json'}
    )

    assert response.status == '201 CREATED'
    assert json.loads(response.data) == {
        'id': 1,
        'name': u'Abraham Lincoln',
        'birth_date': u'1809-02-12',
        'computers': [],
    }

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
