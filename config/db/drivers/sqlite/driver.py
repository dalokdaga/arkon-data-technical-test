import sqlite3
from config.db.drivers.base_driver import BaseDBDriver


class DriverDB(BaseDBDriver):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.connection_string)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
