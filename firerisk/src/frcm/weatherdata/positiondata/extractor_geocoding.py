import json
from frcm.datamodel.model import Location
import numpy as np

from frcm.weatherdata.extractor import LocationExtractor

class GeoCodingExtractor(LocationExtractor):
    
    def extract_coordinates(self, geocode_response_str: str) -> list[Location]:
        coordinates = []
        geocode_response = json.loads(geocode_response_str)
        resultater = geocode_response['adresser']
        for result in resultater:
            lat = result['representasjonspunkt']['lat']
            lon = result['representasjonspunkt']['lon']
            location = Location(latitude=lat, longitude=lon)
            coordinates.append(location)
        
        return coordinates