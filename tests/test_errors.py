"""Test error handling."""
import muckr_api.errors
from muckr_api.extensions import database


def test_handle_error_rolls_back_on_internal_error(app, mocker):
    mock_session = mocker.patch.object(database, "session")
    muckr_api.errors.handle_error(Exception())
    mock_session.rollback.assert_called_once_with()


def test_handle_error_returns_status_500_on_internal_error(app):
    response = muckr_api.errors.handle_error(Exception())
    assert response.status_code == 500
    assert response.json == {"error": "Internal Server Error"}
    assert response.mimetype == "application/json"
