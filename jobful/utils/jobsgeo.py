import sys
import pymongo

import imp
import geo
mongo_connector = imp.load_source('mc', '../utils/mongo_connector.py')

db=mongo_connector.get_db()

def persist_company_coordinates(key, item):
    company_coordinates = db.company_coordinates  
    body = dict(key.items() + item.items())
    company_coordinates.update(key, body, upsert=True)   
  
def persist_coordinates_not_found(doc):
    coordinates_not_found= db.coordinates_not_found
    coordinates_not_found.update(doc, doc,upsert=True) 

def get_coord_companies():
    iter = db.jobs.aggregate([{"$group":{"_id":{"company":"$company","location":"$location"}}}]);
    for doc in iter['result']:
        try:

            coords = geo.coord(doc['_id']['company'] + " " + doc['_id']['location']) 
            if coords is None:
               persist_coordinates_not_found(doc)
            else:
               persist_company_coordinates(doc,coords)
        except:
            print "Unexpected error:", sys.exc_info()[0] 
            continue

def main():
    get_coord_companies()

if __name__ == '__main__':
    main()