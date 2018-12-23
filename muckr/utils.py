'''Common utilities'''
import flask


def jsonify(data):
    response = flask.jsonify(data)
    response.mimetype = 'application/json'
    return response
