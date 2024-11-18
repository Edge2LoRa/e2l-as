import time
from threading import Thread, Lock
import logging
import pandas as pd
import random
import os

log = logging.getLogger(__name__)

class E2LoraBalancer():
    
    def __init__(self, experiment_id):
        self.assigning_algorithm = None
        self.refresh_interval = 1
        self.assignment_table = dict()
        self.experiment_id = experiment_id
        self.update_counter = 0
        self.dataset = None
        self.snapshot_file = None


    def _random_assignment(self):
        dataset_table = pd.read_csv(self.dataset+self.snapshot_file)
        devices_list = dataset_table["NODE_ID"].unique()

        self.assignment_table = dict()
        for device in devices_list:
            self.assignment_table[device] = random.randint(0,49)
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
            if self.update_counter >= self.refresh_interval:
                print("Assigning...")
                self.update_counter = 0
                self._assingment_function()
                print(self.assignment_table)
            time.sleep(2)
            


    def start_assignment_loop(self):
        log.debug("Starting assignment loop")
        t = Thread(target=self._assignment_loop)
        t.start()
        return