import unittest
import datetime

import muckr.app
import muckr.extensions
import muckr.models

class MuckrTestCase(unittest.TestCase):
    def setUp(self):
        self.app = muckr.app.create_app('tests.config')
        self.app_context = self.app.app_context()
        self.app_context.push()
        muckr.extensions.database.create_all()

    def tearDown(self):
        muckr.extensions.database.session.remove()
        muckr.extensions.database.drop_all()
        self.app_context.pop()

    def test_person(self):
        birth_date = datetime.datetime(1970, 1, 1)
        person = muckr.models.Person(
            name='john',
            birth_date=birth_date)

        assert person.name == 'john'
        assert person.birth_date == birth_date

if __name__ == '__main__':
    unittest.main(verbosity=2)
