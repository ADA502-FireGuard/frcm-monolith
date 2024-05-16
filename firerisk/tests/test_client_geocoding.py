# TODO: FIR-67 Set up tests for the Geocoding client and extractor

import unittest

from frcm.weatherdata.positiondata.client_geocoding import GeoCodingClient

class TestClientGeocoding (unittest.TestCase):
    
    def setUp(self) -> None:
        self.client = GeoCodingClient()

    
    def test_send_geocoding_request (self):
        pass


    def test_fetch_coordinates_from_address (self):
        pass


    def test_fetch_coordinates_from_postcode (self):
        pass


    def test_fetch_coordinates_from_postarea (self):
        pass


    def test_fetch_coordinates_from_county (self):
        pass


    def test_fetch_coordinates_from_county_number (self):
        pass

if __name__ == '__main__':
    unittest.main()