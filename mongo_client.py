""" MongoClient to ease some basic pymongo functionalities """
import logging
import statistics
from collections import Counter
from bson.son import SON
from pymongo import MongoClient

class MongoConnection:
    """ MongoConnection initialised from GeoService config file """
    def __init__(self, key, config, connection = None):
        self.logger = logging.getLogger(__name__)
        self.url = 'mongodb://{}:{}'.format(config.get(key, 'Host'),config.getint(key, 'Port'))
        if connection is not None:
            self.connection = connection
        else:
            self.connection = MongoClient(self.url, serverSelectionTimeoutMS=config.getint(key, 'Timeout'))
        self.coll = self.connection[config.get(key, 'DatabaseName')][config.get(key, 'CollectionName')]
        self.index_name = config.get(key, 'IndexName')
        self.scale_factor = config.getint(key, 'ScaleFactor')

    def collection(self):
        """ Return Collection """
        if self.connection is not None:
            return self.coll
        else:
            self.logger.warning("Connection to %s is closed", self.url)

    def _scale(self, num):
        """
         Scale factor for dimension translation to allow insertion of
         locations out of typical lat/lon limits ([-180, 180], [-90,90])
        """
        return num / self.scale_factor

    def _get_stats(self, data):
        stats = {}
        for att, vals in data.items():
            stats[att] = {}
            stats[att]['sum'] = sum(vals)
            stats[att]['mean'] = statistics.mean(vals)
            stats[att]['median'] = statistics.median(vals)
        return stats

    def query(self, point, max_distance, attributes):
        """ Method to ease querying points 'near to' other points """
        result = {}
        for doc in self.coll.find(
            {self.index_name: SON([('$near', [self._scale(point.x), self._scale(point.y)]), 
                                   ('$maxDistance', self._scale(max_distance))])}):
            for att in attributes:
                if att in doc:
                    new_list = result.get(att, [])
                    new_list.append(doc[att])
                    result[att] = new_list

        return self._get_stats(result)

    def close(self):
        """ close connection previously opened """
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            self.logger.info("Closed Connection")
        else:
            self.logger.warning("Can't close connection as it looks already closed")
