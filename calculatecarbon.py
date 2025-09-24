from managecsv import CSVManager
from carboninterface import CarbonInterface

class CarbonCalculator:
    """Calculating carbon emissions from from CSV file data and Carbon Interface API
    """
    def __init__(self):
        """Initialize the CarbonCalculator
        """
        self.csv_manager = CSVManager()
        self.carbon_interface = CarbonInterface()
        
    def calculate_electricity_emissions(self):
        """Calculate electricity emissions

        Returns:
            list: A list of dictionaries containing electricity emissions data
        """
        data = self.csv_manager.electricity_data
        emissions = []
        for i, row in data.iterrows():
            country = row['country']
            state = row['state']
            value = row['electricity_value']
            unit = row['electricity_unit']
            response = self.carbon_interface.estimate_electricity(value, unit, country, state)
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
        """Calculate flight emissions

        Returns:
            list: A list of dictionaries containing flight emissions data
        """
        data = self.csv_manager.flight_data
        emissions = []
        for _, row in data.iterrows():
            passengers = row['passengers']
            departure = row['departure_airport']
            destination = row['destination_airport']
            if row['round_trip'] == True:
                round_trip = True
            else:
                round_trip = False
            response = self.carbon_interface.estimate_flight(passengers, departure, destination, round_trip)
            data_row = {
                'passengers': passengers,
                'departure': departure,
                'destination': destination,
                'round_trip': round_trip,
                'emission': response,
            }
            emissions.append(data_row)
            
        return emissions
    
    def calculate_shipping_emissions(self):
        """Calculate shipping emissions

        Returns:
            list: A list of dictionaries containing shipping emissions data
        """
        data = self.csv_manager.shipping_data
        emissions = []
        for _, row in data.iterrows():
            weight = row['weight_value']
            weight_unit = row['weight_unit']
            distance = row['distance_value']
            distance_unit = row['distance_unit']
            transport_method = row['transport_method']
            response = self.carbon_interface.estimate_shipping(weight, weight_unit, distance, distance_unit, transport_method)
            data_row = {
                'weight': weight,
                'weight_unit': weight_unit,
                'distance': distance,
                'distance_unit': distance_unit,
                'transport_method': transport_method,
                'emission': response
            }
            emissions.append(data_row)

        return emissions
    
    def calculate_vehicle_emissions(self):
        """Calculate vehicle emissions

        Returns:
            list: A list of dictionaries containing vehicle emissions data
        """
        data = self.csv_manager.vehicle_data
        emissions = []
        for _, row in data.iterrows():
            distance = row['distance_value']
            distance_unit = row['distance_unit']
            vehicle_make = row['vehicle_make']
            vehicle_name = row['vehicle_name']
            vehicle_year = row['vehicle_year']
            response = self.carbon_interface.estimate_vehicle(distance, distance_unit, vehicle_make, vehicle_name, vehicle_year)
            data_row = {
                'distance': distance,
                'distance_unit': distance_unit,
                'vehicle_make': vehicle_make,
                'vehicle_name': vehicle_name,
                'vehicle_year': vehicle_year,
                'emission': response
            }
            emissions.append(data_row)
            
        return emissions