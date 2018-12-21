'''Test error handling.'''
import muckr.errors
from muckr.extensions import database


def test_handle_error_rolls_back_on_internal_error(app, mocker):
    mock_session = mocker.patch.object(database, 'session')
    muckr.errors.handle_error(Exception())
    mock_session.rollback.assert_called_once_with()


def test_handle_error_returns_status_500_on_internal_error(app):
    response = muckr.errors.handle_error(Exception())
    assert response.status_code == 500
    assert response.json == {'error': 'Internal Server Error'}
    assert response.mimetype == 'application/json'
