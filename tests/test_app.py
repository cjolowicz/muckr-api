'''Test app module.'''
import muckr.app
import muckr.extensions


def test_import(app):
    attribute, value = muckr.app._import('muckr.extensions.database')
    assert attribute == 'database'
    assert value is muckr.extensions.database
