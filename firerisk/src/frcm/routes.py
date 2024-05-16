from fastapi import APIRouter, Depends
from frcm.kc.auth import verify_user_role
from frcm.logic.logic_handler import LogicHandler
import time
import threading
import inspect

# Start of RestAPI implementation. Below is defined all the paths that are used to access the FireGuard Cloud Service.
router = APIRouter()
logic_handler: LogicHandler = LogicHandler()# Init LogicHandler object.

# Authenticates user.
@router.get("/authenticate")
async def authenticate(user: bool = Depends(verify_user_role)):
    return { "message": "User authenticated." }

# Default for services selection. Returns JSON containing info on available services, input variables required and return values.
@router.get("/services")
async def services():
    return {
        "message": "FireGuard services",
        "rawdata": get_function_query_parm(raw_data),
        "area": {
            "gps": get_function_query_parm(gps),
            "postcode": get_function_query_parm(postcode),
            "address": get_function_query_parm(address)
            }
        }

# Default for area selection. Returns expected input variables for the area service functions.
@router.get("/area")
async def area():
    #TODO UPDATE THESE PATHS TO THE CORRECT VERSIONS
    return {
        "message": "Område tjeneste frå FireGuard, brannrisiko basert på værdata frå lokasjonar.",
        "area": {
            "gps": get_function_query_parm(gps),
            "postcode": get_function_query_parm(postcode),
            "address": get_function_query_parm(address)
        }
    }

# Calculates fire risk based on raw data supplied by the user.
@router.post("/rawdata")
async def raw_data(temp: float, temp_forecast: float, humidity: float, humidity_forecast: float, wind_speed: float, wind_speed_forecast: float, timestamp: str, timestamp_forecast: str, lon: float, lat: float):
    print("Accepted request for raw data")
    data: dict = {
        "temp": temp,
        "temp_forecast": temp_forecast,
        "humidity": humidity,
        "humidity_forecast": humidity_forecast,
        "wind_speed": wind_speed,
        "wind_speed_forecast": wind_speed_forecast,
        "timestamp": timestamp,
        "timestamp_forecast": timestamp_forecast,
        "lon": lon,
        "lat": lat
    }
    result: list

    # Make a key and queue a request.
    with threading.Lock():
        key = logic_handler.handle_request(req_type="rawdata", data=data)
        print("Sent request for raw data")

    # Have the thread continuously check if the temporary storage has updated to contain a list of FireRiskPredictions. Once this is the case, return the results stored.
    while True:
        time.sleep(1)
        with threading.Lock():
            print(f"Waiting for result . . . {key}")
            if type(logic_handler.results[key]) == list:
                result = logic_handler.results[key]
                logic_handler.results.pop(key)
                break
    return result


# Calculates fire risk based on GPS coordinates supplied by the user.
@router.get("/area/gps")
async def gps (lon: float, lat: float, days: float = 1.0):
    print("Accepted request for GPS")
    data: dict = {
        "lon": lon,
        "lat": lat,
        "days": days
    }
    result: list

    # Make a key and queue a request.
    with threading.Lock():
        key = logic_handler.handle_request(req_type="gps", data=data)
        print("Sent request for GPS")

    # Have the thread continuously check if the temporary storage has updated to contain a list of FireRiskPredictions. Once this is the case, return the results stored.
    while True:
        time.sleep(1)
        with threading.Lock():
            print(f"Waiting for result . . . {key}")
            if type(logic_handler.results[key]) == list:
                result = logic_handler.results[key]
                logic_handler.results.pop(key)
                break
    return result


# Calculates fire risk based on multiple GPS coordinates supplied by the user.
@router.get("/area/multiple_gps")
async def multiple_gps(lon: list[float], lat: list[float], days: list[float]):
    print("Accepted request for multiple GPS")
    if not len(lon) == len(lat) or not len(lon) == len(days) or not len(lat) == len(days):
        return "Error: size of lon, lat and/or days do not match."
    data: dict = {}
    result: list

    # Pack the data from the lists into the data dictionary for the request.
    for i in range(0, len(lon)):
        data_point: dict = {
            "lon": lon[i],
            "lat": lat[i],
            "days": days[i]
        }
        data[i] = data_point

    # Make a key and queue a request.
    with threading.Lock():
        key = logic_handler.handle_request(req_type="multiple_gps", data=data)
        print("Sent request for multiple GPS")

    # Have the thread continuously check if the temporary storage has updated to contain a list of FireRiskPredictions. Once this is the case, return the results stored.
    while True:
        time.sleep(1)
        with threading.Lock():
            print(f"Waiting for result . . . {key}")
            if type(logic_handler.results[key]) == list:
                result = logic_handler.results[key]
                logic_handler.results.pop(key)
                break
    return result


# Calculates fire risk based on postcode. Uses separate API to determine coordinates for the post code.
@router.get("/area/postcode")
async def postcode (postal_code: int, days: float):
    print("Accepted request for postal code")
    data: dict = {
        "postal_code": postal_code,
        "days": days
    }
    result: list

    # Make a key and queue a request.
    with threading.Lock():
        key = logic_handler.handle_request(req_type="postal_code", data=data)
        print("Sent request for postal code")

    # Have the thread continuously check if the temporary storage has updated to contain a list of FireRiskPredictions. Once this is the case, return the results stored.
    while True:
        time.sleep(1)
        with threading.Lock():
            print(f"Waiting for result . . . {key}")
            if type(logic_handler.results[key]) == list:
                result = logic_handler.results[key]
                logic_handler.results.pop(key)
                break
    return result

# Calculates fire risk based on address. Uses separate API to determine coordinates for the address.
@router.get("/area/address")
async def address (adr: str, days: float):
    print("Accepted request for address")
    data: dict = {
        "address": adr,
        "days": days
    }
    result: list

    # Make a key and queue a request.
    with threading.Lock():
        key = logic_handler.handle_request(req_type="address", data=data)
        print("Sent request for address")

    # Have the thread continuously check if the temporary storage has updated to contain a list of FireRiskPredictions. Once this is the case, return the results stored.
    while True:
        time.sleep(1)
        with threading.Lock():
            print(f"Waiting for result . . . {key}")
            if type(logic_handler.results[key]) == list:
                result = logic_handler.results[key]
                logic_handler.results.pop(key)
                break
    return result

def get_function_query_parm(func):
    signature = inspect.signature(func)
    return {param_name: str(param.annotation).split("'")[1] for param_name, param in signature.parameters.items()}