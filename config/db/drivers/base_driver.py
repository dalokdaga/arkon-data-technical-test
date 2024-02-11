from sqlalchemy import text
from abc import ABC, abstractmethod
import pandas as pd


class BaseDBDriver(ABC):
    @abstractmethod
    def connect(self):
        """Método abstracto para establecer la conexión con la base de datos."""
        pass

    def disconnect(self):
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Error disconnecting from database: {e}")

    def execute_query(self, query: str, params: tuple = None):
        if params:
            query = query % params        
        df = pd.read_sql_query(text(query), self.conn)
        return df

    def save_data(self, dataframe, table_name, if_exists='replace'):
        try:
            if not self.conn:
                raise Exception("Connection is not established.")
            dataframe.to_sql(table_name, self.conn, if_exists=if_exists)
            self.conn.commit()
        except Exception as e:
            print(f"Error saving data to table: {e}")
