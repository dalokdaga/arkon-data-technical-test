from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.core.handler import ApiHandler
from app.api.core.serializers.all_response import AllResponse
from app.api.core.serializers.id_response import DataOneResponse


router = APIRouter()


@router.get("/wifi_access_points", response_class=JSONResponse)
def wifi_access_points(cologne: str = None) -> AllResponse:
    if cologne:        
        return ApiHandler.data_by_cologne_handler(cologne=cologne)
    else:        
        return ApiHandler.list_all_handler()


@router.get("/wifi_access_points_by_id/{id}", response_class=JSONResponse)
def wifi_access_points_by_id(id: str) -> DataOneResponse:
    return ApiHandler.data_by_id_handler(id=id)


@router.get("/wifi_ordered_by_proximity/latitude/{latitude}/longitude/{longitude}")
def wifi_ordered_by_proximity(latitude: float, longitude: float) -> AllResponse:
    return ApiHandler.wifi_ordered_by_proximity_handler(**{
        "latitude": latitude,
        "longitude": longitude 
    })
