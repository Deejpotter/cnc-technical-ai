import pymongo
from bson.objectid import ObjectId
from IDataManager import IDataManager


class MongoDataManager(IDataManager):
    def __init__(self, uri, db_name, collection_name):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create(self, data):
        # MongoDB specific create operation
        pass

    def get(self, id):
        # MongoDB specific get operation
        return self.collection.find_one({"_id": ObjectId(id)})

    def find(self, query):
        # MongoDB specific find operation
        pass

    def update(self, id, data):
        # MongoDB specific update operation
        pass

    def delete(self, id):
        # MongoDB specific delete operation
        pass
