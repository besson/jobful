import urllib, urllib2, json

def coord(address):
   params = {
                'address' : clean(address),
                'sensor' : 'false',
        }  
   url = 'https://maps.googleapis.com/maps/api/geocode/json?' + urllib.urlencode(params)
   response = urllib2.urlopen(url)
   result = json.load(response)
   try:
        return result['results'][0]['geometry']['location']
   except:
        return None

def clean(address):
     return(address.strip().replace(".com",""))


def main():
        #print(decode_address_to_coordinates("850+Cherry+Ave,+San+Bruno")) ok
        print(coord("walmart office san bruno"))
    
if __name__ == '__main__':
    main()

