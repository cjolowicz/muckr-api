'''Error handlers.'''
from werkzeug.http import HTTP_STATUS_CODES
from flask import jsonify

from muckr.extensions import database


def error_response(status_code, message=None, details=None):
    status = HTTP_STATUS_CODES.get(status_code, 'Unknown error')

    payload = {'error': status}
    if message:
        payload['message'] = message
    if details:
        payload['details'] = details

    response = jsonify(payload)
    response.status_code = status_code
    response.mimetype = 'application/json'
    return response


def handle_error(error):
    # If a HTTPException, pull the `code` attribute; default to 500
    status_code = getattr(error, 'code', 500)
    if status_code == 500:
        database.session.rollback()
    return error_response(status_code)
