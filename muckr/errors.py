from werkzeug.http import HTTP_STATUS_CODES
from flask import jsonify


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
