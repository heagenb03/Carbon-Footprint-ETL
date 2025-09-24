import subprocess
from mysqlmanager import MySQLManager

def main():
    """Main function to run the ETL process and R data visualization
    """
    mysql_manager = MySQLManager()
    mysql_manager.insert_electricity_emissions()
    mysql_manager.insert_flight_emissions()
    mysql_manager.insert_shipping_emissions()
    mysql_manager.insert_vehicle_emissions()
    
    try:
        subprocess.check_call(['Rscript', 'data_visualization.R'])
    except subprocess.CalledProcessError as error:
        print(f'Error occurred while running R script: {error}')

if __name__ == '__main__':
    main()