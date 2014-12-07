import pymongo
import sys
import career
import imp
mongo_connector = imp.load_source('x', '../jobful/utils/mongo_connector.py')

db=mongo_connector.get_db()

def persist(doc):
    tabSal = db.jobsSal
    tabSal.insert(doc)   

def getSalaries():

    iter = db.jobs.aggregate([{"$group":{"_id":{"title":"$title","location":"$location"}, "n":{"$sum":"1"}}}]);
    for doc in iter['result']:
        try:
            item = career.getSalary(career.crawl(doc['_id']['title'], doc['_id']['location'])) 
            doc = dict(doc.items() + item.items())
            print doc
            persist(doc)
        except:
            print doc
            print "Unexpected error:", sys.exc_info()[0] 
            continue

def main():
        getSalaries()

    
if __name__ == '__main__':
    main()

