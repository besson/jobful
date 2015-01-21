import geo
import pymongo
import imp
mongo_connector = imp.load_source('mc', '../utils/mongo_connector.py')
db=mongo_connector.get_db()

def save_company_coord(key, coords):
    company_coordinates = db.company_coordinates 
    body = dict(key.items() + coords.items())
    company_coordinates.update(key, body, upsert=True)   
  
def save_not_found_coord(doc):
    coordinates_not_found = db.coordinates_not_found
    coordinates_not_found.update(doc, doc,upsert=True) 

def find_company_coord(company, location):
    return(_find_save_company_coord(company, location))

def _find_save_company_coord(company, location):
    coords = _find_company_coord(company, location)
    if coords == None:
       coords = geo.coord(location) 
       if coords != None:
           key = dict([('company', company), ('location', location)])
           save_company_coord (key, coords)
           coords = _find_company_coord(company, location)
       else:
           save_not_found_coord(key)
    return coords

def _find_company_coord(company, location):
    company_coordinates = db.company_coordinates 
    _get_query = {"$and": [{"company": company}, {"location": location}]}
    _fields_query = {"lat":1, "lng":1, "_id":0}
    if db.company_coordinates.find(_get_query).count() > 0:
       coords = db.company_coordinates.find(_get_query, _fields_query)[0]
       return coords
    else:
       return None

def main():
    print(find_company_coord("amazon","US, TN, Lebanon"))

if __name__ == '__main__':
    main()