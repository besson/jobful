from solr import Solr
from datetime import date
from utils.mongo_connector import get_db


def index():
    s = Solr('http://localhost:8983/solr/jobs')
    db = get_db()

    for job in db.jobs.find():
        job["id"] = str(job.pop("_id"))
        job["updated_at"] = date.today()

        #try:
        company = job["company"]
        location = job["location"]
        geo = job.pop("coordinate") 
        print geo
        job["geo_location"] = "%f,%f" % (geo["lat"], geo["lng"])
        print job["geo_location"]
        #job = {"id": "mydoc", "company": "Me"} 
        #print type(job)
        s.add(job)
        #except Exception as e:
        #    print e
        #    pass


index()
