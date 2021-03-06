import threading
import sys
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('hr.chatbot.db')

class MongoClient(object):
    def __init__(self):
        self.client = None

def init_mongo_client(mongoclient, host='localhost', port=27017):
    import pymongo
    def _init_mongo_client(mongoclient):
        while mongoclient.client is None:
            mongoclient.client = pymongo.MongoClient(
                'mongodb://{}:{}/'.format(host, port),
                socketTimeoutMS=1000,
                serverSelectionTimeoutMS=1000)
            try:
                mongoclient.client.admin.command('ismaster')
                logger.warn("Activate mongodb")
            except pymongo.errors.ConnectionFailure:
                logger.error("Server not available")
                mongoclient.client = None
            time.sleep(0.2)

    timer = threading.Timer(0, _init_mongo_client, (mongoclient,))
    timer.daemon = True
    timer.start()
    logger.info("Thread starts")

def get_mongo_client(host='localhost', port=27017):
    mongoclient = MongoClient()
    init_mongo_client(mongoclient, host, port)
    return mongoclient

if __name__ == '__main__':
    mongoclient = get_mongo_client()
    while mongoclient.client is None:
        time.sleep(0.1)
    print mongoclient.client.server_info()
