import datetime
import dateutil.parser

from frcm.datamodel.model import Location, FireRiskPrediction
from frcm.frcapi import FireRiskAPI

class LogicHandlerUtils():

    def __init__(self) -> None:
        pass    


    def calculate_from_gps_and_timedelta (self, frc: FireRiskAPI, lon: float, lat: float, days: float) -> FireRiskPrediction:
        """
            Takes lon, lat and days and compacts them to location, then calculates using this and returns the firerisk prediction.
        """
        timedelta: datetime.timedelta = datetime.timedelta(days=days)
        print(f"lon: {lon} \t lat: {lat} \t days: {days} \t timedelta: {timedelta}")
        location: Location = Location(longitude=lon, latitude=lat)
        return frc.compute_now(location=location, obs_delta=timedelta)
    

    def calculate_from_raw_data (self, frc: FireRiskAPI, temp: float, temp_forecast: float, humidity: float, humidity_forecast: float, wind_speed: float, wind_speed_forecast: float, timestamp: str, timestamp_forecast: str, lon: float, lat: float):
        """
            Takes raw data input from the user and calculates it, returns the firerisk prediction.
        """
        return frc.compute_from_raw_data(temp=temp, temp_forecast=temp_forecast, humidity=humidity, humidity_forecast=humidity_forecast, wind_speed=wind_speed, wind_speed_forecast=wind_speed_forecast, timestamp=dateutil.parser.parse(timestamp), timestamp_forecast=dateutil.parser.parse(timestamp_forecast), lon=lon, lat=lat)