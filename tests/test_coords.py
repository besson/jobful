import unittest
from unittest import TestCase
import imp
geo = imp.load_source('geo', '../jobful/utils/geo.py')

class TestGetCoordinates(TestCase):
    def test_valid_address(self):
        addresses = ["850 Cherry Avenue, San Bruno", "WALMART OFFICE SAN BRUNO"]
        for element in addresses:
            ret = geo.coord(element)
            self.assertEqual(-122, int(ret["lng"]))
            self.assertEqual(37, int(ret["lat"]))
