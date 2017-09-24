'''
GeoService.

Usage:
 geoservice.py ingester <config> <input> [-v]
 geoservice.py endpoint <config> [-v]
 geoservice.py  -h | --help
 geoservice.py --version

Options:
  -h --help     Show this screen.
  -v  Verbose mode
'''
import csv
from configparser import ConfigParser
import logging
import atexit
from docopt import docopt
from point import Point
from mongo_client import MongoConnection


def csv_reader(file_name):
    """ Csv Generator """
    with open(file_name, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row_dict in reader:
            yield {k: int(v) for k, v in row_dict.items()}

def run_endpoint(key, cfg):
    """ Run REST Endpoint Mode """
    import geoservice_endpoint
    geoservice_endpoint.CONNECTION = MongoConnection(key, cfg)
    atexit.register(geoservice_endpoint.CONNECTION.close)
    geoservice_endpoint.app.run(host='0.0.0.0')

def run_ingester(key, cfg, input_csv):
    """ Run Ingestion Mode """
    from geoservice_ingester import Ingester

    conn = MongoConnection(key, cfg)
    collection = conn.collection()

    ingester = Ingester(collection, config.get(key, 'IndexName'))
    ingester.create_index()

    for row in csv_reader(input_csv):
        ingester.ingest(Point(row.pop('x') / config.getint(key, 'ScaleFactor'),
                              row.pop('y') / config.getint(key, 'ScaleFactor')), row)

    conn.close()

if __name__ == "__main__":
    LOG_LEVELS = {0: logging.INFO, 1: logging.DEBUG}
    CONFIG_KEY = 'GeoService'
    arguments = docopt(__doc__, version='GeoService 1.0')
    logging.basicConfig(level=LOG_LEVELS[arguments.get('-v')])
    config = ConfigParser()
    config.read(arguments.get('<config>'))
    if arguments.get('ingester'):
        run_ingester(CONFIG_KEY, config, arguments.get('<input>'))
    else:
        run_endpoint(CONFIG_KEY, config)
