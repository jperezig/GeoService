import unittest
import geoservice

class TestGeoService(unittest.TestCase):

    def test_csv_reader(self):
        expected = [
            {'x': 966752, 'y': 526673,
             'attribute1': 17, 'attribute2': 28, 'attribute3': 66,
             'attribute4': 30, 'attribute5': 90, 'attribute6': 28,
             'attribute7': 18, 'attribute8': 30, 'attribute9': 71,
             'attribute10': 88, 'attribute11': 63, 'attribute12': 49,
             'attribute13': 90, 'attribute14': 27, 'attribute15': 60},
            {'x': 460795, 'y': 115292,
             'attribute1': 63, 'attribute2': 6, 'attribute3': 14,
             'attribute4': 19, 'attribute5': 19, 'attribute6': 75,
             'attribute7': 61, 'attribute8': 96, 'attribute9': 3,
             'attribute10': 69, 'attribute11': 57, 'attribute12': 26,
             'attribute13': 93, 'attribute14': 33, 'attribute15': 7}]

        self.assertEqual(
            [d for d in geoservice.csv_reader('test_csv.csv')], expected)
