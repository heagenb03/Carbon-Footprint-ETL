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
        if response.status_code > 201:
            raise Exception('Invalid API Key')
    
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
        if response.status_code > 201:
            raise Exception(f'Error fetching data \n Code: {response.status_code} \n Message: {response.text} \n Data: {data}')
        
        return response.json()

    def parse_data(self, response):
        data = response['data']
        attributes = data['attributes']
        estimate = attributes['carbon_mt']
        return estimate
    
    def fetch_vehicle_make_id(self, vehicle_make):
        url = f'{self.url}/vehicle_makes'
        response = requests.get(url, headers=self._headers)
        if response.status_code > 201:
            raise Exception(f'Error fetching data \n Code: {response.status_code} \n Message: {response.text}')
        
        make_id = None
        data = json.loads(response.text)
        for name in data:
            if name['data']['attributes']['name'] == vehicle_make:
                make_id = name['data']['id']
                return make_id
            
        if make_id == None:
            raise Exception(f'Vehicle make not found: {vehicle_make}')
    
    def fetch_vehicle_model_id(self, vehicle_make_id, vehicle_name, vehicle_year):
        url = f'{self.url}/vehicle_makes/{vehicle_make_id}/vehicle_models'
        response = requests.get(url, headers=self._headers)
        if response.status_code > 201:
            raise Exception(f'Error fetching data \n Code: {response.status_code} \n Message: {response.text}')
        
        model_id = None
        data = json.loads(response.text)
        for name in data:
            if name['data']['attributes']['name'] == vehicle_name and name['data']['attributes']['year'] == vehicle_year:
                model_id = name['data']['id']
                return model_id
        
        if model_id == None:
            raise Exception(f'Vehicle model not found: {vehicle_name} {vehicle_year}')
    
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
                'departure_airport': departure,
                'destination_airport': destination
            }
        ]
        
        if round_trip:
            legs.append(
                {
                    'departure_airport': destination,
                    'destination_airport': departure
                }
            )
        
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
    
    def estimate_vehicle(self, value_distance, unit_distance, vehicle_make, vehicle_name, vehicle_year):
        vehicle_make_id = self.fetch_vehicle_make_id(vehicle_make)
        vehicle_model_id = self.fetch_vehicle_model_id(vehicle_make_id, vehicle_name, vehicle_year)
        
        data = {
            'type': 'vehicle',
            'distance_value': value_distance,
            'distance_unit': unit_distance,
            'vehicle_model_id': vehicle_model_id
        }
        
        response_json = self.fetch_data(data)
        estimate = self.parse_data(response_json)
        return estimate