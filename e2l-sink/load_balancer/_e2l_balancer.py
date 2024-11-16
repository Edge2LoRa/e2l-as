import time
from threading import Thread, Lock
import logging


log = logging.getLogger(__name__)

class E2LoraBalancer():
    
    def __init__(self, experiment_id):
        self.assigning_algorithm = None
        self.refresh_interval = 1
        self.assignment_table = dict()
        self.experiment_id = experiment_id


    def _random_assignment(self):
        return

    def _assign_on_proximity(self):
        return 

    def _balanced_assignment(self):
        return
    

    def _assingment_function(self):
        if self.assigning_algorithm == "Random":
            return self._random_assignment()
        elif self.assigning_algorithm == "Nearest":
            return self._assign_on_proximity()
        elif self.assigning_algorithm == "Balanced":
            return self._balanced_assignment()
        else:
            print("Invalid assigning algorithm")
            return
    
    def _assignment_loop(self):
        while True:
            print("Assigning...")
            self._assingment_function()
            time.sleep(self.refresh_interval*5)


    def start_assignment_loop(self):
        log.debug("Starting assignment loop")
        t = Thread(target=self._assignment_loop)
        t.start()
        return