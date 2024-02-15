from sqlalchemy import create_engine
from app.api.core.exceptions import NoConnectionDatabaseException
from config.db.drivers.base_driver import BaseDBDriver


class DriverDB(BaseDBDriver):
    ''' Driver to create sql queries '''
    def __init__(self, connection_uri):
        self.connection_uri = connection_uri
        self.connect()

    def connect(self):
        ''' Crea una conexión con sqlalchemy '''
        try:            
            engine = create_engine(self.connection_uri)
            self.conn = engine.connect()
        except Exception as e:
            raise NoConnectionDatabaseException(e)
