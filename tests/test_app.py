"""Test app module."""
import muckr_api.app
import muckr_api.extensions


def test_import_returns_name_value_pair(app):
    attribute, value = muckr_api.app._import("muckr_api.extensions.database")
    assert attribute == "database"
    assert value is muckr_api.extensions.database


def test_register_shell_context_registers_database(app):
    context = app.make_shell_context()
    assert "database" in context
    assert context["database"] is muckr_api.extensions.database
