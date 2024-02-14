from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.api.core.handler import ApiHandler
from app.api.core.paginator import Paginator
from app.api.core.serializers.all_response import AllResponse
from app.api.core.serializers.id_response import AccessPoint
from fastapi_pagination.utils import disable_installed_extensions_check

disable_installed_extensions_check()

router = APIRouter()


@router.get("/wifi_access_points", response_model=AllResponse)
def wifi_access_points(
        offset: int = Query(default=0, ge=0), limit: int = Query(default=50, le=1000), 
        cologne: str = None) -> AllResponse:
    results = None
    if cologne:
        results = ApiHandler.data_by_cologne_handler(cologne=cologne)
    else:
        results = ApiHandler.list_all_handler()

    access_points, pagination_info = Paginator.paginate_results(results, offset, limit)
    return AllResponse(access_points=access_points, pagination_info=pagination_info)


@router.get("/wifi_access_points_by_id/{id}", response_class=JSONResponse)
def wifi_access_points_by_id(id: str) -> AccessPoint:
    return ApiHandler.data_by_id_handler(id=id)


@router.get("/wifi_ordered_by_proximity/latitude/{latitude}/longitude/{longitude}", response_model=AllResponse)
def wifi_ordered_by_proximity(
        latitude: float, longitude: float, offset: int = Query(default=0, ge=0), 
        limit: int = Query(default=50, le=1000)) -> AllResponse:
    results = ApiHandler.wifi_ordered_by_proximity_handler(latitude=latitude, longitude=longitude)
    access_points, pagination_info = Paginator.paginate_results(results, offset, limit)
    return AllResponse(access_points=access_points, pagination_info=pagination_info)
