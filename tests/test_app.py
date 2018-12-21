'''Test app module.'''
import muckr.app
import muckr.extensions


def test_import_returns_name_value_pair(app):
    attribute, value = muckr.app._import('muckr.extensions.database')
    assert attribute == 'database'
    assert value is muckr.extensions.database


def test_register_shell_context_registers_database(app):
    context = app.make_shell_context()
    assert 'database' in context
    assert context['database'] is muckr.extensions.database
