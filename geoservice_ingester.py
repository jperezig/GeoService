"""
 Ingestion Module
"""
import json
import logging
from pymongo import GEO2D
from pymongo.errors import ServerSelectionTimeoutError

class Ingester:
    """
     This class is in charge og ingesting from CSV file to Mongo,
     using a 2D euclidean index.
    """
    def __init__(self, collection, index_name):
        self.logger = logging.getLogger(__name__)
        self.collection = collection
        self.index_name = index_name

    def create_index(self):
        """ Create 'loc' index to speedup geospatial searches """
        self.collection.create_index([(self.index_name, GEO2D)])

    def _build_document(self, loc, attributes):
        document = json.loads(json.dumps(attributes))
        document[self.index_name] = [loc.x, loc.y]
        return document

    def bulk_ingest(self, data):
        """ Insert into Mongo in bulk mode """
        docs = [self._build_document(loc, atts) for loc, atts in data]
        try:
            document_ids = self.collection.insert_many(docs).inserted_ids
            self.logger.debug('Inserted batch of documents size: %s %s', len(
                document_ids), document_ids)
            return document_ids
        except ServerSelectionTimeoutError:
            self.logger.error('Cannot connect to collection')
        return -1

    def ingest(self, loc, attributes):
        """ Insert into Mongo """
        try:
            document_id = self.collection.insert_one(
                self._build_document(loc, attributes)).inserted_id
            self.logger.debug('Inserted document: %s', document_id)
            return document_id
        except ServerSelectionTimeoutError:
            self.logger.error('Cannot connect to collection')
        return -1
