"""Common utilities"""
import flask

from muckr_api.errors import APIError


def jsonify(data):
    response = flask.jsonify(data)
    response.mimetype = "application/json"
    return response


def check_unique(query, key, value):
    condition = {key: value}
    if query.filter_by(**condition).first():
        message = "please use a different {key}".format(key=key)
        raise APIError(400, message=message, details={key: message})


def check_unique_on_create(query, data, keys):
    for key in keys:
        check_unique(query, key, data[key])


def check_unique_on_update(query, model, data, keys):
    for key in keys:
        if key in data and data[key] != getattr(model, key):
            check_unique(query, key, data[key])


def paginate(query):
    page = flask.request.args.get("page", 1, type=int)
    per_page = min(flask.request.args.get("per_page", 10, type=int), 100)
    return query.paginate(page, per_page, False)
