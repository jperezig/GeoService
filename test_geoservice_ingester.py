import unittest
from geoservice_ingester import Ingester
from point import Point
import mongomock


class TestIngester(unittest.TestCase):

    def setUp(self):
        self.client = mongomock.MongoClient()
        self.collection = self.client.db.collection
        self.index_name = 'INDEX_NAME'

    def test_ingester(self):
        attributes = {'att1': 1, 'att2': 2, 'att3': 3}
        point = Point(1, 2)
        ingester = Ingester(self.collection, self.index_name)
        ingester.create_index()

        self.assertNotEqual(ingester.ingest(point, attributes), -1)

    def test_bulk_ingester(self):
        data = [(Point(1, 2), {'att1': 1, 'att2': 2, 'att3': 3}),
                (Point(3, 4), {'att1': 1, 'att2': 2, 'att3': 3})]
        ingester = Ingester(self.collection, self.index_name)
        ingester.create_index()

        self.assertEqual(len(ingester.bulk_ingest(data)), len(data))

    def tearDown(self):
        self.client.close()
