import os
import pymongo

mongodb_connection_string = os.getenv("MONGODB_CLIENT")
db = os.getenv("DATABASE")
col = os.getenv("COLLECTION")


def mongo_connect():
    try:
        myclient = pymongo.MongoClient(mongodb_connection_string)
        collection = myclient[db][col]
        return collection
    except pymongo.errors.ConnectionFailure as e:
        print("A database connection issue occurred",e)