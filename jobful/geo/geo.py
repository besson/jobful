import urllib, urllib2, json

def coord(address):
   coord = get_coord_google(address)
   if coord == None:
      coord = get_coord_google(_find_city_state_of_address(address))
   return coord 

def get_coord_google(address):
   params = {
                'address' : _clean(address),
                'sensor' : 'false',
        }  
   url = 'https://maps.googleapis.com/maps/api/geocode/json?' + urllib.urlencode(params)
   print url
   response = urllib2.urlopen(url)
   result = json.load(response)
   #try:

   if result['status'] =='OK':
      return(result['results'][0]['geometry']['location'])
   else:
      return None

   
  #except:

   #     return None

def _find_city_state_of_address(address):
  file_cities = open("cities.dat", "r")
  file_states = open("states.dat", "r")
  cities = file_cities.read().split("\r")
  states = file_states.read().split("\r")
  address_to_find = ""
  for city in cities:
      if city.lower() in address.lower():
        address_to_find = city
        break;
  for s in states:
      state = s.split(";")
      if state[0].lower() in address.lower():
        address_to_find = state[0]
        break;
      if state[1].lower()in address.lower():
        address_to_find = state[0]
        break;
  return (address_to_find)
  

def _clean(address):
     return(address.strip().replace(".com","").encode(encoding='UTF-8'))
