from sqlalchemy import create_engine
from config.db.drivers.base_driver import BaseDBDriver


class DriverDB(BaseDBDriver):
    def __init__(self, connection_uri):
        self.connection_uri = connection_uri
        self.connect()

    def connect(self):
        try:
            # Crear una conexión con sqlalchemy
            engine = create_engine(self.connection_uri)
            self.conn = engine.connect()
        except Exception as e:
            print(f"Error connecting to MySQL database: {e}")
