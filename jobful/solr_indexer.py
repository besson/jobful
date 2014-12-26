from solr import Solr
from datetime import date
from utils.mongo_connector import get_db


def index():
    s = Solr('http://localhost:8983/solr/jobs')
    db = get_db()

    for job in db.jobs.find():
        job["id"] = str(job.pop("_id"))
        job["updated_at"] = date.today()

        try:
            company = job["company"]
            location = job["location"]
            geo = db.company_coordinates.find(_get_query(company, location))[0]

            job["geo_location"] = "%f,%f" % (geo["lat"], geo["lng"])
            print dict(job)

            s.add(dict(job), commit=True)
        except Exception as e:
            print e
            pass


def _get_query(company, location):
    return {"$and": [{"_id.company": company}, {"_id.location": location}]}

index()
