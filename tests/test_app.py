import unittest
import datetime

import muckr_service
import muckr_service.models
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

    def tearDown(self):
        muckr_service.database.session.remove()
        muckr_service.database.drop_all()
        self.app_context.pop()

    def test_person(self):
        birth_date = datetime.datetime(1970, 1, 1)
        person = muckr_service.models.Person(
            name='john',
            birth_date=birth_date)

        assert person.name == 'john'
        assert person.birth_date == birth_date

if __name__ == '__main__':
    unittest.main(verbosity=2)
