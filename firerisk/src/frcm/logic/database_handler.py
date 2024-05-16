import threading
import time
import datetime

from frcm.datamodel.model import FireRiskPrediction, Location

class DatabaseHandler:

    def __init__ (self):
        self.lock = threading.Lock()

        self.init_check_database()
        self.timer_thread = threading.Thread(target=self.database_timer, name="Database-Timer-Thread", daemon=True)
        self.timer_thread.start()


    def open_database ():
        """
            Opens the database.
        """
        #TODO Database handler
        pass


    def close_database ():
        """
            Closes the database.
        """
        #TODO Database handler
        pass


    def init_check_database (self):
        """
            Makes initial checks on the database during startup of the program.
        """
        #TODO Database handler
        pass


    def database_timer (self):
        """
            Runs a timer that checks the items inside the database for expiration and starts the removal- or renewal processes. 
            Also handles checking subscriptions and starts renewal of data- and sending of data processes.
        """
        #TODO Database handler
        while True:
            time.sleep(60)

            with self.lock:
                pass


    def update_database_item (self):
        """
            Updates an item in the database by making a request to the Logic Handler for processing new data.
        """
        #TODO Database handler
        pass


    def remove_database_item (self):
        """
            Removes an item from the database.
        """
        #TODO Database handler
        pass


    def append_database_item (self):
        """
            Adds an item to the database.
        """
        #TODO Database handler
        pass
