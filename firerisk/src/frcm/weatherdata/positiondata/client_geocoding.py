from frcm.datamodel.model import Location
import requests

from frcm.weatherdata.client import LocationDataClient
from frcm.weatherdata.positiondata.extractor_geocoding import GeoCodingExtractor

class GeoCodingClient(LocationDataClient):

    def __init__(self):
        """
            Set enpoints for RestAPI requests for both address- and postcode geocoding.
            Imports ID and secret key for geocoding client from .env file.

            Kartverket "Åpent adresse-API"
            https://ws.geonorge.no/adresser/v1/#/default/get_sok
        """

        self.geocoding_endpoint = 'https://ws.geonorge.no/adresser/v1/sok'
        self.extractor = GeoCodingExtractor()

    def send_geocoding_request (self, parameters):
        """
            Sends request to Kartverket's Geocoding API "Åpent adresse-API" and receives raw data.
        """
        header = {'User-Agent': 'DYNAMIC Firerisk Model'}
        return requests.get(self.geocoding_endpoint, headers=header, params=parameters)
    

    def fetch_coordinates_from_address (self, address: str) -> list[Location]:
        params = {
            'fuzzy': 'false',
            'adressetekst': address,
            'utkoordsys': '4258',
            'treffPerSide': '1',
            'side': '0',
            'filtrer': 'adresser.representasjonspunkt',
            'asciiKompatibel': 'true'
        }

        geocode_response = self.send_geocoding_request(parameters=params)

        coordinates = self.extractor.extract_coordinates(geocode_response_str=geocode_response.text)

        return coordinates
    

    def fetch_coordinates_from_postcode (self, postcode: int, number_of_coords: int = 1) -> list[Location]:
        """
            Requesting coordinates to a postal code will return a list of addresses within that postal code area. The results may span up in the hundreds or even thousands. This amount of coordinates is not considered as usefull, as each of the addresses are within a certain area of each other. It may be interesting in the future to select a couple of coordinates that have the largest gap in coordinates to get a more accurate reading of the entire area, however this is more computationally intensive and should perhaps be limited to certain users.
            For now, we only select to receive the first coordinate and address that matches the postal code, if any, and consider that as representative
        """

        params = {
            'fuzzy': 'false',
            'postnummer': str(postcode),
            'utkoordsys': '4258',
            'treffPerSide': str(number_of_coords),
            'side': '0',
            'filtrer': 'adresser.representasjonspunkt',
            'asciiKompatibel': 'true'
        }

        geocode_response = self.send_geocoding_request(parameters=params)

        coordinates = self.extractor.extract_coordinates(geocode_response_str=geocode_response.text)

        return coordinates


    def fetch_coordinates_from_postarea (self, postarea: str, number_of_coords: int = 1) -> list[Location]:
        """
            Requesting coordinates to a postal area will return a list of addresses within that postal area. The results may span up in the hundreds or even thousands. This amount of coordinates is not considered as usefull, as each of the addresses are within a certain area of each other. It may be interesting in the future to select a couple of coordinates that have the largest gap in coordinates to get a more accurate reading of the entire area, however this is more computationally intensive and should perhaps be limited to certain users.
            For now, we only select to receive the first coordinate and address that matches the postal area, if any, and consider that as representative
        """

        params = {
            'fuzzy': 'false',
            'poststed': postarea,
            'utkoordsys': '4258',
            'treffPerSide': str(number_of_coords),
            'side': '0',
            'filtrer': 'adresser.representasjonspunkt',
            'asciiKompatibel': 'true'
        }

        geocode_response = self.send_geocoding_request(parameters=params)

        coordinates = self.extractor.extract_coordinates(geocode_response_str=geocode_response.text)

        return coordinates


    def fetch_coordinates_from_county (self, county: str, number_of_coords: int = 1) -> list[Location]:
        """
            Requesting coordinates to a county will return a list of addresses within that county. The results may span up in the hundreds or even thousands. This amount of coordinates is not considered as usefull, as each of the addresses are within a certain area of each other. It may be interesting in the future to select a couple of coordinates that have the largest gap in coordinates to get a more accurate reading of the entire area, however this is more computationally intensive and should perhaps be limited to certain users.
            For now, we only select to receive the first coordinate and address that matches the county, if any, and consider that as representative
        """

        params = {
            'fuzzy': 'false',
            'kommunenavn': county,
            'utkoordsys': '4258',
            'treffPerSide': str(number_of_coords),
            'side': '0',
            'filtrer': 'adresser.representasjonspunkt',
            'asciiKompatibel': 'true'
        }

        geocode_response = self.send_geocoding_request(parameters=params)

        coordinates = self.extractor.extract_coordinates(geocode_response_str=geocode_response.text)

        return coordinates


    def fetch_coordinates_from_county_number (self, county_number: int, number_of_coords: int = 1) -> list[Location]:
        """
            Requesting coordinates to a county number will return a list of addresses within that county number. The results may span up in the hundreds or even thousands. This amount of coordinates is not considered as usefull, as each of the addresses are within a certain area of each other. It may be interesting in the future to select a couple of coordinates that have the largest gap in coordinates to get a more accurate reading of the entire area, however this is more computationally intensive and should perhaps be limited to certain users.
            For now, we only select to receive the first coordinate and address that matches the county number, if any, and consider that as representative
        """

        params = {
            'fuzzy': 'false',
            'kommunenummer': str(county_number),
            'utkoordsys': '4258',
            'treffPerSide': str(number_of_coords),
            'side': '0',
            'filtrer': 'adresser.representasjonspunkt',
            'asciiKompatibel': 'true'
        }

        geocode_response = self.send_geocoding_request(parameters=params)

        coordinates = self.extractor.extract_coordinates(geocode_response_str=geocode_response.text)

        return coordinates
