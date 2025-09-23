from managecsv import CSVManager
from calculatecarbon import CarbonCalculator
from carboninterface import CarbonInterface
from mysqlmanager import MySQLManager

def main():
    mysql_manager = MySQLManager()
    mysql_manager.insert_electricity_emissions()
    mysql_manager.insert_flight_emissions()
    mysql_manager.insert_shipping_emissions()
    mysql_manager.insert_vehicle_emissions()
    
if __name__ == '__main__':
    main()