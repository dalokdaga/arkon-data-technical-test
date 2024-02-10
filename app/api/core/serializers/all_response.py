from pydantic import BaseModel


class AllResponse(BaseModel):
    access_points: list
