from utils.mongo_connector import get_db
from bson.objectid import ObjectId
import sys

raw_results = sys.argv[1]
db = get_db()

for line in open(raw_results):
    data = line.split(",")
    _id = data[0]
    category = data[-1].strip()

    db.jobs.update({"_id": ObjectId(_id)}, {"$set": {"category": category}})
