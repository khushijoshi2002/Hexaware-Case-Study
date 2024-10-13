import sys
import os

# Add parent directory of 'dao' to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



import pyodbc
from util.DBPropertyUtil import PropertyUtil

class DBConnection:
    connection=None

    @staticmethod
    def getConnection():
        if DBConnection.connection is None:
            try:
                connection_string = PropertyUtil.getPropertyString()
                DBConnection.connection = pyodbc.connect(connection_string)
            except pyodbc.Error as e:
                print(f"Connection Failed: {e}")
        else:
            print("Connection Already Established")
            
        return DBConnection.connection


