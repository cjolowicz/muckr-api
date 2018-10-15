import unittest
import json

import muckr_service
import muckr_service.config

class TestConfig(muckr_service.config.Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class MuckrServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = muckr_service.create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        muckr_service.database.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        muckr_service.database.session.remove()
        muckr_service.database.drop_all()
        self.app_context.pop()

    def test_get_person(self):
        response = self.client.get('/api/person')
        assert json.loads(response.data) == {
            'num_results': 0,
            'objects': [],
            'page': 1,
            'total_pages': 0
        }

    def test_post_person(self):
        person = {
            'name': u'Abraham Lincoln',
            'birth_date': u'1809-02-12',
        }

        response = self.client.post(
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
    unittest.main(verbosity=2)
