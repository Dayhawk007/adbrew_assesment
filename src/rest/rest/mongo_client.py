from pymongo import MongoClient
import os

class MongoDBClient:
    def __init__(self, db_name):
        mongo_uri = f"mongodb://{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}"
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def find_all(self, collection_name, projection=None):
        return list(self.get_collection(collection_name).find({}, projection))

    def insert_one(self, collection_name, document):
        self.get_collection(collection_name).insert_one(document)

    def delete_many(self, collection_name, filter):
        return self.get_collection(collection_name).delete_many(filter)
