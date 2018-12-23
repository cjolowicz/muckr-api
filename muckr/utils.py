'''Common utilities'''
import flask

from muckr.errors import APIError


def jsonify(data):
    response = flask.jsonify(data)
    response.mimetype = 'application/json'
    return response


def check_unique(model_class, key, value):
    condition = {key: value}
    if model_class.query.filter_by(**condition).first():
        message = 'please use a different {key}'.format(key=key)
        raise APIError(400, message=message, details={key: message})


def check_unique_on_create(model_class, data, keys):
    for key in keys:
        check_unique(model_class, key, data[key])


def check_unique_on_update(model_class, model, data, keys):
    for key in keys:
        if key in data and data[key] != getattr(model, key):
            check_unique(model_class, key, data[key])
