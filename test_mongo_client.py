import unittest
from configparser import ConfigParser
from collections import Counter
from mongo_client import MongoConnection
from point import Point
import mongomock

class TestMongoClient(unittest.TestCase):

    def setUp(self):
        self.config = ConfigParser()
        self.key = 'GeoService'
        self.config.read('geoservice.conf')
        self.connection = MongoConnection(
            self.key, self.config, connection=mongomock.MongoClient())

    def test_collection(self):
        self.assertIsNotNone(self.connection.collection())

    def test_closed_collection(self):
        self.connection.close()
        self.assertIsNone(self.connection.collection())

    def test_get_stats(self):
        expected = {'attribute1': {'sum': 15, 'mean': 3, 'median': 3},
                    'attribute2': {'sum': 40, 'mean': 8, 'median': 8}}
        stats = self.connection._get_stats({'attribute1':[1,2,3,4,5], 'attribute2':[6,7,8,9,10]})
        self.assertEqual(stats, expected)

    def test_query(self):
        self.assertEqual(self.connection.query(
            Point(1, 2), 1000000, ['att1', 'att2']), {})
