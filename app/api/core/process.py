
from app.api.core.component.consult_access_componet import ConsultAccessComponent



class ApiProcess:
    @staticmethod
    def list_all_process(offset: int, limit: int) -> dict:
        return ConsultAccessComponent.all_info_run(offset, limit)

    @staticmethod
    def data_by_id_process(id: str) -> dict:
        return ConsultAccessComponent.by_id_run(id)

    @staticmethod
    def data_by_cologne_process(cologne: str, offset: int, limit: int) -> dict:
        return ConsultAccessComponent.by_cologne_run(cologne, offset, limit)

    @staticmethod
    def wifi_ordered_by_proximity_process(latitude: float, longitude: float, offset: int, limit: int) -> list:
        return ConsultAccessComponent.proximity_run(latitude, longitude, offset, limit)