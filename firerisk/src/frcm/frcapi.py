import datetime

from frcm.datamodel.model import FireRiskPrediction, Location, WeatherData, WeatherDataPoint, Observations, Forecast
from frcm.weatherdata.client import WeatherDataClient
import frcm.fireriskmodel.compute


class FireRiskAPI:

    def __init__(self, client: WeatherDataClient):
        self.client = client
        self.timedelta_ok = datetime.timedelta(days=1) # TODO: when during a day is observations updated? (12:00 and 06:00)
        # TODO (NOTE): Short term forecast updates every 3rd hour with long term forecast every 12th hour at 12:00 and 06:00
        self.interpolate_distance = 720

    def compute(self, wd: WeatherData) -> FireRiskPrediction:

        return frcm.fireriskmodel.compute.compute(wd)

    def compute_now(self, location: Location, obs_delta: datetime.timedelta) -> FireRiskPrediction:

        time_now = datetime.datetime.now()
        start_time = time_now - obs_delta

        observations = self.client.fetch_observations(location, start=start_time, end=time_now)

        #print(observations)

        forecast = self.client.fetch_forecast(location)

        #print(forecast)

        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)

        #print(wd.to_json())

        prediction = self.compute(wd)

        return prediction

    def compute_now_period(self, location: Location, obs_delta: datetime.timedelta, fct_delta: datetime.timedelta):
        pass

    def compute_period(self, location: Location, start: datetime, end: datetime) -> FireRiskPrediction:
        pass

    def compute_period_delta(self, location: Location, start: datetime, delta: datetime.timedelta) -> FireRiskPrediction:
        pass

    def compute_from_raw_data(self, temp: float, temp_forecast: float, humidity: float, humidity_forecast: float, wind_speed: float, wind_speed_forecast: float, timestamp: datetime, timestamp_forecast: datetime, lon: float, lat: float) -> FireRiskPrediction:
        # Define location
        location = Location(latitude=lat, longitude=lon)

        # Define observations
        wdp_observation = WeatherDataPoint(temperature=temp, humidity=humidity, wind_speed=wind_speed, timestamp=timestamp)
        data_observations = [wdp_observation]
        observations = Observations(source="userData", location=location, data=data_observations)

        # Define forecast
        wdp_forecast = WeatherDataPoint(temperature=temp_forecast, humidity=humidity_forecast, wind_speed=wind_speed_forecast, timestamp=timestamp_forecast)
        data_forecast = [wdp_forecast]
        forecast = Forecast(location=location, data=data_forecast)

        wd = WeatherData(created=timestamp, observations=observations, forecast=forecast)

        prediction = self.compute(wd)

        return prediction
        
