import abc

from frcm.datamodel.model import Observations, Forecast, Location


class Extractor:
    @abc.abstractmethod
    def extract_observations(self, data: str) -> Observations:
        pass

    @abc.abstractmethod
    def extract_forecast(self, data: str) -> Forecast:
        pass


class LocationExtractor:
    @abc.abstractmethod
    def extract_coordinates (self, data: str) -> Location:
        pass
