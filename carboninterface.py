import os
import json
import requests
import constants

from dotenv import load_dotenv
load_dotenv()

class CarbonInterface:
    def __init__(self):
        self.api_key = os.getenv('CARBON_INTERFACE_API_KEY')
        self.url = constants.CARBON_API_URL
        self._auth()
        
    def _auth(self):
        url = f'{self.url}/auth'
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        response = requests.get(url, headers=headers)
        return response.status_code if response.status_code == 200 else None
    
    @property
    def _headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def fetch_data(self, data):
        json_data = json.dumps(data)
        url = f'{self.url}/estimates'
        response = requests.post(url, data=json_data, headers=self._headers)
        return response.json()

    def parse_data(self, response):
        data = response['data']
        attributes = data['attributes']
        return attributes['carbon_mt']
    
    def fetch_vehicle_id(self, vehicle_name):
        url = f'{self.url}/vehicle_makes'
        response = requests.get(url, headers=self._headers)
        data = response.json()
        for vehicle in data:
            if vehicle['data']['attributes']['name'] == vehicle_name:
                return vehicle['data']['id']
            
        return None
    
    def estimate_eletricity(self, value, unit, country, state=None):
        data = {
            'type': 'electricity',
            'electricity_value': value,
            'electricity_unit': unit,
            'country': country,
        }
        
        if state:
            data['state'] = state
        
        response_json = self.fetch_data(data)
        estimate = self.parse_data(response_json)
        return estimate

    def estimate_flight(self, passengers, departure, destination, round_trip=False):
        legs = [
            {
                'departure': departure,
                'destination': destination
            }
        ]
        
        if round_trip:
            legs.append({
                'departure': destination,
                'destination': departure
            })
        
        data = {
            'type': 'flight',
            'passengers': passengers,
            'legs': legs
        }
        
        response_json = self.fetch_data(data)
        estimate = self.parse_data(response_json)
        return estimate
    
    def estimate_shipping(self, value_weight, unit_weight, value_distance, unit_distance, transport_method):
        data = {
            'type': 'shipping',
            'weight_value': value_weight,
            'weight_unit': unit_weight,
            'distance_value': value_distance,
            'distance_unit': unit_distance,
            'transport_method': transport_method
        }
        
        response_json = self.fetch_data(data)
        estimate = self.parse_data(response_json)
        return estimate
    
    def estimate_vehicle(self, value_distance, unit_distance, vehicle_make):
        vehicle_id = self.fetch_vehicle_id(vehicle_make)
        
        data = {
            'type': 'vehicle',
            'distance_value': value_distance,
            'distance_unit': unit_distance,
            'vehicle_id': vehicle_id
        }
        
        response_json = self.fetch_data(data)
        estimate = self.parse_data(response_json)
        return estimate
    
API = CarbonInterface()