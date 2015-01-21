import sys
import pymongo
import imp
import company_coordinates

mongo_connector = imp.load_source('mc', '../utils/mongo_connector.py')

db=mongo_connector.get_db()


def update_jobs_coord():
    cont = 1
    iter = db.jobs.aggregate([
                              {"$match": {"coordinate": { "$exists": False}}}, 
                              {"$group": {"_id": {"company":"$company","location":"$location"}}}
                            ]);
    print len(iter)
    for doc in iter['result']:
        #try: 
            if (doc["_id"]):
              coords = company_coordinates.find_company_coord(doc["_id"]["company"], doc['_id']['location']) 
              if coords is not None:
                 db.jobs.update(
                                { "company": doc['_id']['company'],
                                  "location":doc['_id']['location']}, 
                                  {"$set":{"coordinate": coords}},
                                   multi=True
                                )
              print cont 
              cont = cont + 1
        #except:
        #    print "Unexpected error:", sys.exc_info()[0] 
        #    continue

def main():
    update_jobs_coord()

if __name__ == '__main__':
    main()