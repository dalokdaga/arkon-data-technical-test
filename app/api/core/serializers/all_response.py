from typing import List
from pydantic import BaseModel

from app.api.core.serializers.id_response import AccessPoint


class AllResponse(BaseModel):
    access_points: List[AccessPoint]
    pagination_info: dict
