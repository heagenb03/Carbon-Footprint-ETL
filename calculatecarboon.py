from managecsv import CSVManager
from carboninterface import CarbonInterface

class CarbonCalculator:
    def __init__(self):
        self.csv_manager = CSVManager()
        self.carbon_interface = CarbonInterface()
        
    def calculate_electricity_emissions(self):
        data = self.csv_manager.electricity_data
        emissions = []
        for _, row in data.iterrows():
            country = row['country']
            state = row['state']
            value = row['electricity_value']
            unit = row['electricity_unit']
            response = self.carbon_interface.estimate_eletricity(value, unit, country, state)
            data_row = {
                'country': country,
                'state': state,
                'value': value,
                'unit': unit,
                'emission': response
            }
            emissions.append(data_row) 
            
        return emissions
    
    def calculate_flight_emissions(self):
        data = self.csv_manager.flight_data
        emissions = []
        for _, row in data.iterrows():
            passengers = row['passengers']
            departure = row['departure_airport']
            destination = row['destination_airport']
            round_trip = True if row['round_trip'] == 'true' else False
            response = self.carbon_interface.estimate_flight(passengers, departure, destination, round_trip)
            emissions.append(response)
            
        return emissions
    
    def calculate_shipping_emissions(self):
        data = self.csv_manager.shipping_data
        emissions = []
        for _, row in data.iterrows():
            weight = row['weight_value']
            weight_unit = row['weight_unit']
            distance = row['distance_value']
            distance_unit = row['distance_unit']
            transport_method = row['transport_method']
            response = self.carbon_interface.estimate_shipping(weight, weight_unit, distance, distance_unit, transport_method)
            emissions.append(response)

        return emissions
    
    def calculate_vehicle_emissions(self):
        data = self.csv_manager.vehicle_data
        emissions = []
        for _, row in data.iterrows():
            distance = row['distance_value']
            distance_unit = row['distance_unit']
            vehicle_make = row['vehicle_make']
            response = self.carbon_interface.estimate_vehicle(distance, distance_unit, vehicle_make)
            emissions.append(response)
            
        return emissions