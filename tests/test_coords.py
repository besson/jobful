import unittest
from unittest import TestCase
import imp
geo = imp.load_source('geo', '../jobful/utils/geo.py')

class TestGetCoordinates(TestCase):
    def test_valid_address(self):
        addresses = ["850 Cherry Avenue, San Bruno", "WALMART OFFICE SAN BRUNO"]
        for element in addresses:
            ret = geo.coord(element)
            self.assertEqual(int(ret["lng"]),-122)
            self.assertEqual(int(ret["lat"]),37)
