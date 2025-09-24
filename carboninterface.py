import os
import json
import requests
import constants
from dotenv import load_dotenv

load_dotenv()
class CarbonInterface:
    """Object for interacting with the Carbon API
    """
    def __init__(self):
        """Initialize CarbonInterface
        """
        self.api_key = os.getenv('CARBON_INTERFACE_API_KEY')
        self.url = constants.CARBON_API_URL
        self._auth()
        
    def _auth(self):
        """Authenticate with the Carbon API

        Raises:
            Exception: If authentication fails
        """
        url = f'{self.url}/auth'
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code > 201:
            raise Exception('Invalid API Key')
    
    @property
    def _headers(self):
        """Return headers for API requests

        Returns:
            dict: Headers to include in API requests
        """
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def fetch_data(self, data):
        """Fetch data from the Carbon API

        Args:
            data (dict): Data to send in the API request

        Raises:
            Exception: If the API request fails

        Returns:
            dict: The API response
        """
        json_data = json.dumps(data)
        url = f'{self.url}/estimates'
        response = requests.post(url, data=json_data, headers=self._headers)
        if response.status_code > 201:
            raise Exception(f'Error fetching data \n Code: {response.status_code} \n Message: {response.text} \n Data: {data}')

        return response.json()

    def parse_data(self, response):
        """Parse the API response data

        Args:
            response (dict): The API response

        Returns:
            float: The estimated carbon emissions
        """
        data = response['data']
        attributes = data['attributes']
        estimate = attributes['carbon_mt']
        return estimate
    
    def fetch_vehicle_make_id(self, vehicle_make):
        """Fetch the vehicle make ID from the Carbon API

        Args:
            vehicle_make (str): The name of the vehicle make

        Raises:
            Exception: If the API response is invalid
            Exception: If the vehicle make is not found

        Returns:
            str: The ID of the vehicle make
        """
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
            
        # Check if make_id was found    
        if make_id == None:
            raise Exception(f'Vehicle make not found: {vehicle_make}')
    
    def fetch_vehicle_model_id(self, vehicle_make_id, vehicle_name, vehicle_year):
        """Fetch the vehicle model ID from the Carbon API

        Args:
            vehicle_make_id (str): The ID of the vehicle make
            vehicle_name (str): The name of the vehicle model
            vehicle_year (int): The year of the vehicle model

        Raises:
            Exception: If the API response is invalid
            Exception: If the vehicle model is not found

        Returns:
            str: The ID of the vehicle model
        """
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

        # Check if model_id was found
        if model_id == None:
            raise Exception(f'Vehicle model not found: {vehicle_name} {vehicle_year}')

    def estimate_electricity(self, value, unit, country, state=None):
        """Estimate the carbon emissions for electricity consumption

        Args:
            value (float): The amount of electricity consumed
            unit (str): The unit of measurement for electricity (e.g., kWh)
            country (str): The country where the electricity is consumed
            state (str, optional): The state where the electricity is consumed. Defaults to None.

        Returns:
            float: The estimated carbon emissions
        """
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
        """Estimate the carbon emissions for a flight

        Args:
            passengers (int): The number of passengers on the flight
            departure (str): The IATA code of the departure airport
            destination (str): The IATA code of the destination airport
            round_trip (bool, optional): Whether the flight is a round trip. Defaults to False.

        Returns:
            float: The estimated carbon emissions
        """
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
        """Estimate the carbon emissions for shipping

        Args:
            value_weight (float): The weight of the shipment
            unit_weight (str): The unit of measurement for weight (kg or lb)
            value_distance (float): The distance of the shipment
            unit_distance (str): The unit of measurement for distance (km or mi)
            transport_method (str): The method of transport (ship, truck, train, or plane)

        Returns:
            float: The estimated carbon emissions
        """
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
        """Estimate the carbon emissions for a vehicle trip

        Args:
            value_distance (float): The distance of the trip
            unit_distance (str): The unit of measurement for distance (km or mi)
            vehicle_make (str): The make of the vehicle
            vehicle_name (str): The model name of the vehicle
            vehicle_year (int): The year the vehicle was manufactured

        Returns:
            float: The estimated carbon emissions
        """
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