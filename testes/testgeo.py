import unittest
import imp
geo = imp.load_source('x', '../utils/geo.py')

class testgeo(unittest.TestCase):
    def tests(self):
        addresses = ["850 Cherry Avenue, San Bruno", "WALMART OFFICE SAN BRUNO"]
        for element in addresses:
            ret = geo.coord(element)
            self.assertEqual(int(ret["lng"]),-122)
            self.assertEqual(int(ret["lat"]),37)
