import boto3
import requests
import pandas as pd
import os 
import constants

CARBON_API_KEY = os.getenv('CARBON_INTERFACE_API_KEY')

def load_activites():
    electricity_data = pd.read_csv(constants.ELECTRICITY_DATA_PATH)
    flight_data = pd.read_csv(constants.FLIGHT_DATA_PATH)
    shipping_data = pd.read_csv(constants.SHIPPING_DATA_PATH)
    vehicle_data = pd.read_csv(constants.VEHICLE_DATA_PATH)
    
    return electricity_data, flight_data, shipping_data, vehicle_data