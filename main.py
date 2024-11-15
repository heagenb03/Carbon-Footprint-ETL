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
            unit = row['electricity_unit']
            value = row['electricity_value']
            response = self.carbon_interface.estimate_eletricity(value, unit, country, state)
            emissions.append(response)
            
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
    
API = CarbonCalculator()
print(API.calculate_flight_emissions())