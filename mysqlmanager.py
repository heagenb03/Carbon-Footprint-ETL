import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv()

mydb = mysql.connector.connect(
    host='localhost',
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DB')
)

mycursor = mydb.cursor()

#mycursor.execute('CREATE TABLE electricity (id INT AUTO_INCREMENT PRIMARY KEY, country VARCHAR(255), state VARCHAR(255), electricity_value FLOAT, electricity_unit VARCHAR(255), carbon_emission FLOAT, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
mycursor.execute('SHOW TABLES')

for x in mycursor:
    print(x)