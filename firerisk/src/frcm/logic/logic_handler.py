import threading
import time
import random
import datetime

from frcm.frcapi import FireRiskAPI
from frcm.datamodel.model import FireRiskPrediction, Location
from frcm.weatherdata.positiondata.client_geocoding import GeoCodingClient
from frcm.weatherdata.client_met import METClient
from frcm.logic.utils import LogicHandlerUtils
from frcm.logic.database_handler import DatabaseHandler

class LogicHandler():

    """
    THREAD PROTECTED VARIABLES

    db_handler
    active_threads
    waiting_list
    
    """

    def __init__(self) -> None:

        self.lock = threading.Lock()
        self.waiting_list = []
        self.max_threads = 3 # constant
        self.active_threads = 0

        # Database handler object
        self.db_handler = DatabaseHandler()

        # Start looping through the waiting list and check every second if there is an open slot for a request to be handled.
        self.queue_manager = threading.Thread(target=self.queue_handler, name="Queue-Manager-Thread", daemon=True) #TODO: Should this be marked as a background thread or should it keep the program running? For now it is set as background thread.
        self.queue_manager.start()

        # dictionary for storing result values
        self.results: dict = {}


    def finish_request (self, data: list):
        pass


    def process_request(self, data):
        """
            Accepts the input data for a request and processes it. Prints out a message indicating that it is being handled.
            Determines first if data exists in Database already.
            If not, determines what type of request is being amde, e.g. gps coordinates, rawdata, address, etc.
            Sends the request to appriopriate subclass for coordinating with the Geo- and Met clients.
            Returns resulting calculation once the entire process is done.
        """
        print(f"--> Request-key: {data[0]}, type: '{data[1]}' is being processed by {threading.current_thread().name}")

        # Extract request data
        randomized_key = data[0]
        req_type = data[1]
        request_data: dict = data[2]

        """ This will come later in the code, however it requires finishing implementing the database handler.
        with self.lock:
            if self.lookup_database():
                result = "shit" #TODO Ve so snill å husk å fjerna denne før me leverer <3
                self.results[randomized_key] = result
                req_type = "finished"
        """

        # Define objects for storing locations and fire risk predictions.
        locations: list[Location]
        result: list[FireRiskPrediction] = []

        # Define objects for storing logic util, clients to other cloud services and firerisk api.
        logic_utils = LogicHandlerUtils()
        client_geo = GeoCodingClient()
        client_met = METClient()
        frc = FireRiskAPI(client=client_met)

        """
            Determine what kind of request this is, and from there process the request based upon the expected input data for such a request.
        """
        # Single gps point request
        if req_type == "gps":
            lon: float = request_data["lon"]
            lat: float = request_data["lat"]
            days: float = request_data["days"]
            result.append(logic_utils.calculate_from_gps_and_timedelta(frc=frc, lon=lon, lat=lat, days=days))

        # Multiple gps points requested
        elif req_type == "multiple_gps":
            points: list = list(request_data["multiple_gps"].values())
            
            for p in points:
                lon: float = p["lon"]
                lat: float = p["lat"]
                days: float = p["days"]
                
                result.append(logic_utils.calculate_from_gps_and_timedelta(frc=frc, lon=lon, lat=lat, days=days))

        # Calculate multiple as many points as defined from a postal code. Default is 1 coordinate per postal code.
        elif req_type == "postal_code":
            postal_code = request_data["postal_code"]
            days = request_data["days"]
            points = client_geo.fetch_coordinates_from_postcode(postcode=postal_code, number_of_coords=1)
            for p in points:
                result.append(frc.compute_now(location=p, obs_delta=datetime.timedelta(days=days)))

        # Calculate point from a given address.
        elif req_type == "address":
            adr = request_data["address"]
            days = request_data["days"]
            points = client_geo.fetch_coordinates_from_address(address=adr)
            for p in points:
                result.append(frc.compute_now(location=p, obs_delta=datetime.timedelta(days=days)))

        # Calculate single location from raw data supplied by the user
        elif req_type == "rawdata":
            temp: float = request_data["temp"]
            temp_forecast: float = request_data["temp_forecast"]
            humidity: float = request_data["humidity"]
            humidity_forecast: float = request_data["humidity_forecast"]
            wind_speed: float = request_data["wind_speed"]
            wind_speed_forecast: float = request_data["wind_speed_forecast"]
            timestamp: str = request_data["timestamp"]
            timestamp_forecast: str = request_data["timestamp_forecast"]
            lon: float = request_data["lon"]
            lat: float = request_data["lat"]

            result.append(logic_utils.calculate_from_raw_data(frc=frc, temp=temp, temp_forecast=temp_forecast, humidity=humidity, humidity_forecast=humidity_forecast, wind_speed=wind_speed, wind_speed_forecast=wind_speed_forecast, timestamp=timestamp, timestamp_forecast=timestamp_forecast, lon=lon, lat=lat))

        # Test case
        elif req_type == "test":
            result = ["test else"] 

        #
        #TODO TEMPORARY SLEEP TIMER FOR DEBUGGING, TESTING AND SHOWCASING. REMOVE LATER!
        #
        #time.sleep(5)

        print(f"--> {threading.current_thread().name} Finished handling request with key {randomized_key}")

        with threading.Lock():
            self.active_threads -= 1
            self.results[randomized_key] = result


    def handle_request(self, req_type: str, data: dict) -> int:
        """
            Takes in information on request type and data associated with it, determines how many requests are currently being handled, and either starts a new thread to handle the request or adds the request to the waiting list.
            Creates a randomized key used to access the results once the request has been handled.
            Returns the randomized key, and temporarily sets the results dictionary's value corresponding to the key to be "placeholder" to simplify the requesting thread's checking if the request has been handled and finished by determining the type of the result stored.

            For input data, format as dictionary with the following possible key values:
            data: {
                "lon": float,
                "lat": float,
                "days": float,

                "multiple_gps": {
                    "1": {
                        "lon": float,
                        "lat": float,
                        "days": float
                    },
                    ...
                    ...
                    ...
                    "n": {}
                },

                "postal_code": int,
                "address": str,

                "temp": float,
                "temp_forecast": float,
                "humidity": float,
                "humidity_forecase": float,
                "wind_speed": float,
                "wind_speed_forecase": float,
                "timestamp": str,
                "timestamp_forecase": str
            }
        """
        randomized_key: int

        with threading.Lock():
            # Create randomized key. Checks if randomized key exists already in the dictionary. In that case keep getting new randomized key and checking for duplicates and stops immediately when there is no longer a duplicate key in the dictionary.
            randomized_key = random.randint(0, 10000000)
            while randomized_key in list(self.results.keys()):
                randomized_key = random.randint(0, 10000000)
            self.results[randomized_key] = "placeholder"

            if self.active_threads < self.max_threads:
                self.active_threads += 1
                # Start a new thread
                thread = threading.Thread(target=self.process_request, args=([randomized_key, req_type, data],), name=f"Thread-key-{randomized_key}")
                thread.start()
                
            else:
                # Add to waiting list
                self.waiting_list.append([randomized_key, req_type, data])
                print(f"--> Request type: {req_type} data: {data} added to waiting list with key: {randomized_key}")

        return randomized_key


    def queue_handler(self):
        """
            Locks the current thread.
            Checks if number of active threads is less than max threads + 1 allowed at a single time.
            Checks if there are requests on the waiting list. If so, starts a thread with the request. If not, breaks out of the while loop.
        """
        while True:
            time.sleep(1)
            with self.lock:
                if self.waiting_list and self.active_threads < (self.max_threads + 1):
                    request = self.waiting_list.pop(0)
                    self.active_threads += 1
                    thread = threading.Thread(target=self.process_request, args=(request,), name=f"Thread-key-{request[0]}")
                    thread.start()
                    
                    print(f"--> Request {request} started from waiting list!")
                else:
                    continue
    

    def lookup_database (self) -> bool:
        """
            Looks through the database if the data requested already exists, returns either True or False
        """
        # TODO 
        return False
    

    def withdraw_database_data (self) -> list[FireRiskPrediction]:
        """
            Retrieves data from the database
        """
        pass

