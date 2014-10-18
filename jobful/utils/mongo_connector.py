import pymongo


def get_db():
    client = pymongo.MongoClient("localhost", 27017)
    return client.jobful
