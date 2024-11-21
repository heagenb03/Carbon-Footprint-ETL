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

manager = MySQLManager()
manager.insert_electricity_emissions()