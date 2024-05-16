import unittest
import threading
import time

from frcm.logic.logic_handler import LogicHandler
from frcm.datamodel.model import FireRiskPrediction

class TestLogicHandler (unittest.TestCase):
    def setUp(self) -> None:
        self.logic_handler = LogicHandler()

    
    def test_handle_request (self):

        # Create requests for testing that the thread creation and queue handler functions as it should.
        with threading.Lock():
            request1 = self.logic_handler.handle_request("test", ["data1", "data2"])
            request2 = self.logic_handler.handle_request("test", ["data1", "data2"])
            request3 = self.logic_handler.handle_request("test", ["data1", "data2"])
            request4 = self.logic_handler.handle_request("test", ["data1", "data2"])
            request5 = self.logic_handler.handle_request("test", ["data1", "data2"])
        
        requests: list = [request1, request2, request3, request4, request5]

        # Loops and sleeps 1 second, checks if all of the requests in the list have finished. If so, breaks out of the loop and proceeds with tests.
        while True:
            time.sleep(1)
            with threading.Lock():
                has_finished: bool = True
                for r in requests:
                    if not type(self.logic_handler.results[r]) == list:
                        has_finished = False

                if has_finished:
                    break
        
        # Check that the results store the correct value.
        with threading.Lock():
            self.assertEqual(self.logic_handler.results[request1], ["test else"])
            self.assertEqual(self.logic_handler.results[request2], ["test else"])
            self.assertEqual(self.logic_handler.results[request3], ["test else"])
            self.assertEqual(self.logic_handler.results[request4], ["test else"])
            self.assertEqual(self.logic_handler.results[request5], ["test else"])

        #expected_firerisk_key1 = [FireRiskPrediction()]

        #self.assertEqual(self.logic_handler.results[key1], )

        #TODO: Finish tests after API functions are properly implemented into handle_request


    def test_process_request (self):
        pass

    def test_lookup_database (self):
        pass 