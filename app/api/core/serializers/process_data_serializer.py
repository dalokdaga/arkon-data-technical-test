from pydantic import BaseModel, validator
from datetime import datetime


class ProcessData(BaseModel):
    date_base: str

    @validator('date_base')
    def validate_fecha(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("The date is not in the correct format (YYYY-MM-DD)")
        return v    


class ProcessDataResponse(BaseModel):
    message: str
