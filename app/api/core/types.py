import strawberry
from typing import List, Optional


@strawberry.type
class AccessPoint:
    id: str
    programa: str
    fecha_instalacion: Optional[str]
    latitud: float
    longitud: float
    colonia: str
    alcaldia: str
    distancia: Optional[float] = None


@strawberry.type
class PaginationInfo:
    total_items: int
    total_pages: int
    current_page: int
    items_per_page: int


@strawberry.type
class AllResponse:
    access_points: List[AccessPoint]
    pagination_info: PaginationInfo


@strawberry.type
class DataOneReponse:
    data_one: AccessPoint
