# main.py
from typing import Optional
import strawberry
from app.api.core.handler import ApiHandler
from app.api.core.paginator import Paginator
from app.api.core.types import AccessPoint, DataOneReponse, PaginationInfo, AllResponse  # Importa las clases de tipo desde types.py

@strawberry.type
class Query:
    @strawberry.field
    def wifi_access_points(
        offset: int = 0, limit: int = 50, cologne: Optional[str] = None
    ) -> AllResponse:
        results = None
        if cologne:
            results = ApiHandler.data_by_cologne_handler(cologne=cologne)
        else:
            results = ApiHandler.list_all_handler()

        # Convertir los resultados a instancias de AccessPoint
        access_points = [AccessPoint(**ap) for ap in results]

        # Paginar los resultados
        access_points, pagination_info = Paginator.paginate_results(access_points, offset, limit)
        pagination_info = PaginationInfo(**pagination_info)
        return AllResponse(access_points=access_points, pagination_info=pagination_info)

    @strawberry.field
    def wifi_access_points_by_id(id: str) -> AccessPoint:        
        data = ApiHandler.data_by_id_handler(id=id)        
        return AccessPoint(**data)


    @strawberry.field
    def wifi_ordered_by_proximity(
        latitude: float, longitude: float, offset: int = 0, limit: int = 50
    ) -> AllResponse:
        results = ApiHandler.wifi_ordered_by_proximity_handler(latitude=latitude, longitude=longitude)
        access_points, pagination_info = Paginator.paginate_results(results, offset, limit)
        access_points = [AccessPoint(**ap) for ap in access_points]
        pagination_info = PaginationInfo(**pagination_info)
        return AllResponse(access_points=access_points, pagination_info=pagination_info)

# Crea el esquema GraphQL
schema = strawberry.Schema(query=Query)
