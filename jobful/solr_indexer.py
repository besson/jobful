from solr import Solr
from datetime import date
from utils.mongo_connector import get_db


def index():
    s = Solr('http://localhost:8983/solr/jobs')
    today = date.today().isoformat()
    db = get_db()

    for job in db.jobs.find({"updated_at": today}):
        job["id"] = str(job.pop("_id"))
        job["updated_at"] = date.today()
        print dict(job)
        s.add(dict(job), commit=True)

index()
