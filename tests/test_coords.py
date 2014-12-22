import unittest
import imp
geo = imp.load_source('geo', '../utils/geo.py')

class Test_coords(unittest.TestCase):
    def test_address(self):
        addresses = ["850 Cherry Avenue, San Bruno", "WALMART OFFICE SAN BRUNO"]
        for element in addresses:
            ret = geo.coord(element)
            self.assertEqual(int(ret["lng"]),-122)
            self.assertEqual(int(ret["lat"]),37)
