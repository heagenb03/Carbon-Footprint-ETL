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

mycursor.execute('ALTER TABLE vehicle MODIFY COLUMN distance_value FLOAT')