# main.py
from typing import Optional
import strawberry
from app.api.core.handler import ApiHandler
from app.api.core.types import AccessPoint, PaginationInfo, AllResponse


@strawberry.type
class Query:
    @strawberry.field
    def wifi_access_points(
        offset: int = 0, limit: int = 50, colony: Optional[str] = None
    ) -> AllResponse:
        results = None
        if colony:
            results = ApiHandler.data_by_colony_handler(colony=colony, offset=offset, limit=limit)
        else:
            results = ApiHandler.list_all_handler(offset=offset, limit=limit)

        access_points = [AccessPoint(**ap) for ap in results["access_points"]]
        pagination_info = PaginationInfo(**results["pagination_info"])
        return AllResponse(access_points=access_points, pagination_info=pagination_info)

    @strawberry.field
    def wifi_access_points_by_id(id: str) -> AccessPoint:        
        data = ApiHandler.data_by_id_handler(id=id)        
        return AccessPoint(**data)

    @strawberry.field
    def wifi_ordered_by_proximity(
        latitude: float, longitude: float, offset: int = 0, limit: int = 50
    ) -> AllResponse:
        results = ApiHandler.wifi_ordered_by_proximity_handler(
            latitude=latitude, longitude=longitude, offset=offset, limit=limit)
        access_points = [AccessPoint(**ap) for ap in results["access_points"]]
        pagination_info = PaginationInfo(**results["pagination_info"])
        return AllResponse(access_points=access_points, pagination_info=pagination_info)


schema = strawberry.Schema(query=Query)
