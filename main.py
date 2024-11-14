from managecsv import CSVManager
from carboninterface import CarbonInterface

class CarbonCalculator:
    def __init__(self):
        self.csv_manager = CSVManager()
        self.carbon_interface = CarbonInterface()