'''# Purpose: Used to establish a connection to a
     MySQL database and provide methods to execute SQL queries'''
import json
import os

import mysql.connector

class SQLConnection:
    '''# Stores an SQL connection, providing interface 
        methods that perform SQL sanitization and error handling'''
    def __init__(self):
        # Load our database configurations from the config file
        db_configs = None
        script_path = os.path.dirname(os.path.abspath(__file__))
        parent_directory_path = os.path.dirname(script_path)
        config_path = parent_directory_path + "/config/db_config.json"
        with open(config_path, "r") as config_file:
            db_configs = json.load(config_file)
        # Extract the database configurations
        self.host = db_configs['host']
        self.username = db_configs['user']
        self.password = db_configs['password']
        self.database = db_configs['database']
        self.connection = None

    def connect(self):
        '''# Connect to the MySQL database'''
        try:
            self.connection = mysql.connector.connect(\
                user=self.username,password=self.password,\
                host=self.host,database=self.database)
            print("Connected to MySQL database")
        except AttributeError as err:
            print(f"Error: {err}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def disconnect(self):
        '''# Disconnect from the MySQL database'''
        if self.connection:
            self.connection.close()
            print("Disconnected from MySQL database")
        else:
            print("No active connection to close")

    def execute_update(self, sql, data=None):
        '''# Execute an update query'''
        if not self.connection:
            print("No active connection. Please connect first.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
            self.connection.commit()
            cursor.close()
            print("Update executed successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def execute_select(self, sql, data=None):
        '''# Execute a select query'''
        result = None
        if not self.connection:
            print("No active connection. Please connect first.")
            return None

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
            result = cursor.fetchall()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise
        return result
