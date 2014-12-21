import sys
import pymongo

import imp
import geo
mongo_connector = imp.load_source('x', '../utils/mongo_connector.py')

db=mongo_connector.get_db()

def persistgeo(key, item):
    ccoord = db.ccoord  
    body = dict(key.items() + item.items())
    ccoord.update(key, body, upsert=True)   
  
def persistNF(doc):
    ccoordnf= db.ccoordnf
    ccoordnf.update(doc, doc,upsert=True) 

def getCompanies():
    iter = db.jobs.aggregate([{"$group":{"_id":{"company":"$company","location":"$location"}}}]);
    for doc in iter['result']:
        try:

            coords = geo.coord(doc['_id']['company'] + " " + doc['_id']['location']) 
            if coords is None:
               persistNF(doc)
            else:
               persistgeo(doc,coords)
        except:
            print "Unexpected error:", sys.exc_info()[0] 
            continue

def main():
        getCompanies()

if __name__ == '__main__':
    main()