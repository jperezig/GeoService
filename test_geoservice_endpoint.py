import unittest
import json
from configparser import ConfigParser
import mongomock
from mongo_client import MongoConnection
import geoservice_endpoint


class TestGeoServiceEndpoint(unittest.TestCase):

    def setUp(self):
        geoservice_endpoint.app.testing = True
        self.app = geoservice_endpoint.app.test_client()
        self.config = ConfigParser()
        self.key = 'GeoService'
        self.config.read('geoservice.conf')
        self.connection = MongoConnection(
            self.key, self.config, connection=mongomock.MongoClient())

    def test_right_validator(self):
        req = '{"x":460795, "y":115292, "max_distance":10000, "attributes": ["attribute1","attribute2","attribute3"]}'
        validator = geoservice_endpoint.validator()
        self.assertTrue(validator.validate(json.loads(req)))

    def test_wrong_validator(self):
        req = '{"x":460795, "y":115292, "max_distance":"10000", "attributes": ["attribute1","attribute2","attribute3"]}'
        validator = geoservice_endpoint.validator()
        self.assertFalse(validator.validate(json.loads(req)))

    def test_no_route(self):
        self.assertEqual(self.app.post('/').status_code, 404)

    def test_route_no_connection(self):
        geoservice_endpoint.CONNECTION = None
        self.assertEqual(self.app.post('/search').status_code, 500)

    def test_route_no_data(self):
        geoservice_endpoint.CONNECTION = self.connection
        self.assertEqual(self.app.post('/search').status_code, 400)

    def test_route_invalid_request(self):
        geoservice_endpoint.CONNECTION = self.connection
        req = '{"x":460795, "y":115292, "max_distance":"10000", "attributes": ["attribute1","attribute2","attribute3"]}'
        self.assertEqual(self.app.post('/search', data=req,
                                       content_type='application/json').status_code, 400)

    def test_route_valid_request(self):
        geoservice_endpoint.CONNECTION = self.connection
        req = '{"x":460795, "y":115292, "max_distance":10000, "attributes": ["attribute1","attribute2","attribute3"]}'
        self.assertEqual(self.app.post('/search', data=req,
                                       content_type='application/json').status_code, 200)
