import os
import mysql.connector
from dotenv import load_dotenv
from calculatecarboon import CarbonCalculator

load_dotenv()
class MySQLManager:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host='localhost',
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB')
        )
        self.mycursor = self.mydb.cursor()
        
        self.calculate_carbon = CarbonCalculator()

    def insert_electricity_emissions(self):
        emissions = self.calculate_carbon.calculate_electricity_emissions()
        sql = 'INSERT INTO electricity (country, state, electricity_value, electricity_unit, carbon_emission) VALUES (%s, %s, %s, %s, %s)'
        for emission in emissions:
            val = (emission['country'], emission['state'], emission['value'], emission['unit'], emission['emission'])
            self.mycursor.execute(sql, val)
            
        self.mydb.commit()

    def insert_flight_emissions(self):
        emissions = self.calculate_carbon.calculate_flight_emissions()
        print(emissions)
        sql = 'INSERT INTO flight (passengers, departure, destination, round_trip, carbon_emission) VALUES (%s, %s, %s, %s, %s)'
        for emission in emissions:
            val = (emission['passengers'], emission['departure'], emission['destination'], emission['round_trip'], emission['emission'])
            self.mycursor.execute(sql, val)

        self.mydb.commit()
    
    def insert_shipping_emissions(self):
        emissions = self.calculate_carbon.calculate_shipping_emissions()
        sql = 'INSERT INTO shipping (weight_value, weight_unit, distance_value, distance_unit, transport_method, carbon_emission) VALUES (%s, %s, %s, %s, %s, %s)'
        for emission in emissions:
            val = (emission['weight'], emission['weight_unit'], emission['distance'], emission['distance_unit'], emission['transport_method'], emission['emission'])
            self.mycursor.execute(sql, val)
            
        self.mydb.commit()
    
    def insert_vehicle_emissions(self):
        emissions = self.calculate_carbon.calculate_vehicle_emissions()
        sql = 'INSERT INTO vehicle (distance_value, distance_unit, vehicle_make, vehicle_name, vehicle_year, carbon_emission) VALUES (%s, %s, %s, %s, %s, %s)'
        for emission in emissions:
            val = (emission['distance'], emission['distance_unit'], emission['vehicle_make'], emission['vehicle_name'], emission['vehicle_year'], emission['emission'])
            self.mycursor.execute(sql, val)

        self.mydb.commit()
        
manager = MySQLManager()
manager.insert_vehicle_emissions()