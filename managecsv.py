import pandas as pd
import constants

class CSVManager:
    def __init__(self):
        self.electricity_data, self.flight_data, self.shipping_data, self.vehicle_data = self._load_activites()
    
    def _load_activites(self):
        electricity_data = pd.read_csv(constants.ELECTRICITY_DATA_PATH)
        flight_data = pd.read_csv(constants.FLIGHT_DATA_PATH)
        shipping_data = pd.read_csv(constants.SHIPPING_DATA_PATH)
        vehicle_data = pd.read_csv(constants.VEHICLE_DATA_PATH)
        
        return electricity_data, flight_data, shipping_data, vehicle_data