import pymongo
from pymongo import MongoClient
from collections.abc import Iterable

class MongoDB_connector:

    def __init__(self, url="localhost", port="27017", user="root", password="root"):
        self.MONGODB_URL = f"mongodb://{user}:{password}@{url}:{port}/"
        self.client = None
        self.db = None

    def connect_to_db(self, db_name) -> bool:
        
        if self.is_connected():
            print("Client is already connected.")
            return True

        try:
            self.client = MongoClient(self.MONGODB_URL)
        except pymongo.errors.PyMongoError as py_mongo_error:
            print(f"Error in MongoDB connection: {str(py_mongo_error)}") 
            return False
        
        try:
            self.db = self.client[db_name]
            return True

        except pymongo.errors.PyMongoError as py_mongo_error:
            print(f"Error selecting database {db_name}: {str(py_mongo_error)}") 
            return False

    def is_connected(self) -> bool:

        if self.client is None:
            return False

        try:
            self.client.server_info()
            return True

        except:
            return False

    def disconnnect_from_db(self) -> bool:

        if not self.is_connected():
            print("The client is already closed.")
            return True

        try:
            self.client.close()
            return True

        except pymongo.errors.PyMongoError as py_mongo_error:
            print(f"Error closing connection to db: {str(py_mongo_error)}") 
            return False
        
    def db_list_collection_names(self) -> list:

        if not self.is_connected():
            print("The connection is currently closed.")
            return []

        try:
            return self.db.list_collection_names()
        except pymongo.errors.PyMongoError as py_mongo_error:
            print(f"Error retrieving collection names: {str(py_mongo_error)}") 
            return []

    def db_insert_one_document_in_collection(self, collection_name, document) -> bool:
        
        if not self.is_connected():
            print("The connection is currently closed.")
            return False

        try:
            col = self.db[collection_name]
            col.insert_one(document)
            return True

        except pymongo.errors.PyMongoError as py_mongo_error:
            print(f"Error inserting document in collection {collection_name}: {str(py_mongo_error)}") 
            return False
    
    def db_insert_many_documents_in_collection(self, collection_name, documents) -> bool:

        if not self.is_connected():
            print("The connection is currently closed.")
            return False

        if not isinstance(documents, Iterable):
            print("The documents object is not iterable.")
            return False

        try:
            col = self.db[collection_name]
            col.insert_many(documents)
            return True

        except pymongo.errors.PyMongoError as py_mongo_error:
            print(f"Error inserting documents in collection {collection_name}: {str(py_mongo_error)}") 
            return False
    
    def db_find_in_collection(self, collection_name, filter, projection=None) -> Iterable:

        if not self.is_connected():
            print("The connection is currently closed.")
            return False

        try:
            col = self.db[collection_name]
            cursor = col.find(filter, projection)
            return cursor

        except pymongo.errors.PyMongoError as py_mongo_error:
            print(f"Error while executing the query: {str(py_mongo_error)}") 
            return ""

    def db_find_one_in_collection(self, collection_name, query) -> dict:

        if not self.is_connected():
            print("The connection is currently closed.")
            return False

        try:
            col = self.db[collection_name]
            cursor = col.find_one(query)
            return cursor

        except pymongo.errors.PyMongoError as py_mongo_error:
            print(f"Error while executing the query: {str(py_mongo_error)}") 
            return ""

    def db_update_one_in_collection(self, collection_name, filter_, update_) -> bool:
        
        if not self.is_connected():
            print("The connection is currently closed.")
            return False

        try:
            col = self.db[collection_name]
            col.update_one(filter_, update_)
            return True

        except pymongo.errors.PyMongoError as py_mongo_error:
            print(f"Error while executing the update: {str(py_mongo_error)}") 
            return False

    def db_aggregate_in_collection(self, collection_name, pipeline) -> list:

        if not self.is_connected():
            print("The connection is currently closed.")
            return False

        try:
            col = self.db[collection_name]

            # res = col.find({})
            # aggregation_result = self.db.command('aggregate', 'Segment', pipeline=pipeline)
            aggregation_result = col.aggregate(pipeline)
            return list(aggregation_result)

            self.db.command('aggregate', collection_name, pipeline=pipeline, allowDiskUse=True, cursor={})

        except pymongo.errors.PyMongoError as py_mongo_error:
            print(f"Error while executing the aggregation query: {str(py_mongo_error)}") 
            return []

    def db_drop_collection(self, collection_name) -> bool:
        
        if not self.is_connected():
            print("The connection is currently closed.")
            return False

        try:
            col = self.db[collection_name]
            col.drop()
            return True

        except pymongo.errors.PyMongoError as py_mongo_error:
            print(f"Error while dropping the collection {collection_name}: {str(py_mongo_error)}") 
            return False