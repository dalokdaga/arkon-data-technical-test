import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        try:
            if self.conn:
                self.conn.close()
        except sqlite3.Error as e:
            print(f"Error disconnecting from database: {e}")

    def execute_query(self, query: str, params: tuple):
        if params is None:
            df = pd.read_sql_query(query, self.conn)
        else:
            df = pd.read_sql_query(query, self.conn, params=params)
        return df

    def save_data(self, dataframe, table_name, if_exists='replace'):
        try:
            if not self.conn:
                raise Exception("Connection is not established.")
            dataframe.to_sql(table_name, self.conn, if_exists=if_exists)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving data to table: {e}")
