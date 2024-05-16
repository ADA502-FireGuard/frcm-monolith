import dateutil.parser

from frcm.datamodel.model import WeatherDataPoint, Location


def weatherdata_parse(datadict) -> list[WeatherDataPoint]:

    data = list()

    for item in datadict:

        temperature = item['temperature']
        humidity = item['humidity']
        wind_speed = item['wind_speed']
        timestamp = dateutil.parser.parse(item['timestamp'])

        wd_point = WeatherDataPoint(temperature=temperature,
                                    humidity=humidity,
                                    wind_speed=wind_speed,
                                    timestamp=timestamp)

        data.append(wd_point)

    return data


def postcode_locationdata_parse (datadict) -> Location:
    # TODO: [FIR-34] Implement RestAPI methods. Requires the use of Kartverket's geocoding api.
    pass