import time
from threading import Thread, Lock
import logging
import pandas as pd
import random
import os

log = logging.getLogger(__name__)

import math

def haversine(lat1, lon1, lat2, lon2):
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Differences in coordinates
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    
    # Haversine formula
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in kilometers
    distance = R * c
    return distance



class E2LoraBalancer():
    
    def __init__(self, experiment_id):
        self.assigning_algorithm = None
        self.refresh_interval = 1
        self.assignment_table = dict()
        self.experiment_id = experiment_id
        self.update_counter = 0
        self.dataset = None
        self.snapshot_file = None
        self.lock_assignment = Lock()
        self.gateways_positions = pd.read_csv("./gw-roma-50.csv")


    def _random_assignment(self):
        dataset_table = pd.read_csv(self.dataset+self.snapshot_file)
        devices_list = dataset_table["NODE_ID"].unique()

        self.assignment_table = dict()
        for device in devices_list:
            self.assignment_table[device] = random.randint(0,49)
        return

    def _assign_on_proximity(self):
        self.assignment_table = dict()
        dataset_table = pd.read_csv(self.dataset+self.snapshot_file)
        devices_list = dataset_table["NODE_ID"].unique()

        lat_lon_table = dataset_table[["NODE_ID","lat","lon"]].groupby("NODE_ID").mean()

        for device in devices_list:
            best_gateway = 0
            best_distance = 1000000
            for index,row in self.gateways_positions.iterrows():
                distance = haversine(lat_lon_table.loc[device]["lat"],lat_lon_table.loc[device]["lon"],row["lat"],row["lon"])
                if distance < best_distance:
                    best_distance = distance
                    best_gateway = row['GW_ID']
            self.assignment_table[device] = int(best_gateway)
        
        return 

    def _balanced_assignment(self):
        self.assignment_table = dict()
        dataset_table = pd.read_csv(self.dataset+self.snapshot_file)
        devices_list = dataset_table["NODE_ID"].unique()

        lat_lon_table = dataset_table[["NODE_ID","lat","lon"]].groupby("NODE_ID").mean()

        for device in devices_list:
            gateway_distances = []
            for index,row in self.gateways_positions.iterrows():
                distance = haversine(lat_lon_table.loc[device]["lat"],lat_lon_table.loc[device]["lon"],row["lat"],row["lon"])
                gateway_distances.append((row["GW_ID"],distance))
            
            gateway_distances.sort(key=lambda x: x[1])
            random_nearest = random.randint(0,2)
            self.assignment_table[device] = int(gateway_distances[random_nearest][0])
            

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
                self.lock_assignment.acquire()
                self._assingment_function()
                self.lock_assignment.release()
            


    def start_assignment_loop(self):
        log.debug("Starting assignment loop")
        t = Thread(target=self._assignment_loop)
        t.start()
        return