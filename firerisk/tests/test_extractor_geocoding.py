# TODO: FIR-67 Set up tests for the Geocoding client and extractor

import unittest

from frcm.weatherdata.positiondata.extractor_geocoding import GeoCodingExtractor

class TestExtractorGeocoding (unittest.TestCase):
    
    def setUp(self) -> None:
        self.extractor = GeoCodingExtractor()

    
    def test_extract_coordinates (self):
        pass

if __name__ == '__main__':
    unittest.main()