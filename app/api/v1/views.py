from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from app.api.core.handler import ApiHandler
from app.api.core.serializers.all_response import AllResponse
from app.api.core.serializers.id_response import AccessPoint
from fastapi_pagination.utils import disable_installed_extensions_check
from app.api.core.serializers.process_data_serializer import ProcessData, ProcessDataResponse
from app.core.common.commands.console.process_data_command import ProcessDataConsole

disable_installed_extensions_check()

router = APIRouter()


@router.get("/wifi_access_points", response_model=AllResponse)
def wifi_access_points(
        offset: int = Query(default=0, ge=0), limit: int = Query(default=50, le=1000), 
        colony: str = None) -> AllResponse:
    try:
        results = None
        if colony:
            results = ApiHandler.data_by_colony_handler(colony=colony, offset=offset, limit=limit)
        else:
            results = ApiHandler.list_all_handler(offset=offset, limit=limit)

        return AllResponse(access_points=results["access_points"], pagination_info=results["pagination_info"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/wifi_access_points_by_id/{id}", response_class=JSONResponse)
def wifi_access_points_by_id(id: str) -> AccessPoint:
    try:
        return ApiHandler.data_by_id_handler(id=id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    


@router.get("/wifi_ordered_by_proximity/latitude/{latitude}/longitude/{longitude}", response_model=AllResponse)
def wifi_ordered_by_proximity(
        latitude: float, longitude: float, offset: int = Query(default=0, ge=0), 
        limit: int = Query(default=50, le=1000)) -> AllResponse:
    try:
        results = ApiHandler.wifi_ordered_by_proximity_handler(
            latitude=latitude, longitude=longitude, offset=offset, limit=limit)    
        return AllResponse(access_points=results["access_points"], pagination_info=results["pagination_info"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process_data")
def create_invoice(process_data: ProcessData) -> ProcessDataResponse:
    try:
        data = process_data.model_dump()
        ProcessDataConsole.process_data(data.get("date_base"))
        return ProcessDataResponse(message="Process executed correctly")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
