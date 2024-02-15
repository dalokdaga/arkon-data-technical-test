from sqlalchemy import text
from abc import ABC, abstractmethod
import pandas as pd
from app.api.core.exceptions import DatabaseErrorException, NoConnectionDatabaseException


class BaseDBDriver(ABC):
    @abstractmethod
    def connect(self):        
        """Abstract method to establish the connection with the database."""
        pass

    def disconnect(self):
        ''' Method to disconnect the cursor from the data base '''
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            raise DatabaseErrorException(e)

    def execute_query(self, query: str, params: tuple = None):
        ''' Method to execute queries '''
        if params:
            query = query % params        
        df = pd.read_sql_query(text(query), self.conn)
        return df

    def save_data(self, dataframe, table_name, if_exists='replace'):
        ''' Save information to the database by inserting a dataframe '''
        try:
            if not self.conn:
                raise NoConnectionDatabaseException()
            dataframe.to_sql(table_name, self.conn, if_exists=if_exists)
            self.conn.commit()
        except Exception as e:
            raise DatabaseErrorException(e)
