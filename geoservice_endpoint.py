"""
 Definition of GeoService 'search' endpoint.
"""
from flask import Flask, request, jsonify, abort, make_response
from point import Point
from cerberus import Validator


def validator():
    """ validator based in Cerberus """
    schema = {'x': {'type': 'integer'},
              'y': {'type': 'integer'},
              'max_distance': {'type': 'integer'},
              'attributes': {'type': 'list', 'minlength': 1, 'schema': {'type': 'string'}}}
    return Validator(schema)


app = Flask(__name__)

CONNECTION = None

VALIDATOR = validator()



@app.route("/search", methods=['POST'])
def geo_search():
    """ GeoService search route"""
    data = request.get_json()
    if CONNECTION is None:
        abort(make_response(jsonify(message='Connection to Mongo not found'), 500))
    if data is None:
        abort(make_response(jsonify(message='Bad request'), 400))
    if VALIDATOR.validate(data):
        result = CONNECTION.query(
            Point(data['x'], data['y']), data['max_distance'], data['attributes'])
        return jsonify(result)
    else:
        abort(make_response(jsonify(message=VALIDATOR.errors), 400))
