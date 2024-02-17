from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from config.db.conection_orm import Base
from sqlalchemy import ForeignKey


class Colony(Base):
    __tablename__ = 'colonies'
    index = Column(Integer, primary_key=True)
    id = Column(Integer)
    colonia = Column(String)
    alcaldia = Column(String)
    wifi_records = relationship("WifiRecord", back_populates="colony")

    def as_dict(self):
        return {"colonia": self.colonia, "alcaldia": self.alcaldia}


class WifiRecord(Base):
    __tablename__ = 'wifi_logs'
    index = Column(Integer, primary_key=True)
    id = Column(String)    
    id_colonia = Column(Integer, ForeignKey('colonies.id'))
    programa = Column(String)
    fecha_instalacion = Column(Integer)
    latitud = Column(Float)
    longitud = Column(Float)
    colony = relationship("Colony", back_populates="wifi_records")

    def as_dict(self):
        return {
            "id": self.id,            
            "programa": self.programa,
            "fecha_instalacion": self.fecha_instalacion,
            "latitud": self.latitud,
            "longitud": self.longitud            
        }
