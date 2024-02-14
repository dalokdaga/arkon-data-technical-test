from pydantic import BaseModel
from typing import Optional


class AccessPoint(BaseModel):
    id: str
    programa: str
    fecha_instalacion: Optional[str]
    latitud: float
    longitud: float
    colonia: str
    alcaldia: str
