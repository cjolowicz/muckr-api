"""Error handlers."""
from werkzeug.http import HTTP_STATUS_CODES
from flask import jsonify

from muckr_api.extensions import database


class APIError(Exception):
    def __init__(self, status_code, message=None, details=None):
        super().__init__()

        error = HTTP_STATUS_CODES.get(status_code, "Unknown error")

        self.status_code = status_code
        self.payload = {"error": error}

        if message is not None:
            self.payload["message"] = message

        if details is not None:
            self.payload["details"] = details

    def handle(self):
        response = jsonify(self.payload)
        response.status_code = self.status_code
        response.mimetype = "application/json"
        return response


def handle_error(error):
    # If a HTTPException, pull the `code` attribute; default to 500
    status_code = getattr(error, "code", 500)
    if status_code == 500:
        database.session.rollback()
    return APIError(status_code).handle()
