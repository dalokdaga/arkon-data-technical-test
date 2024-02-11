
from app.api.core.component.consult_access_componet import ConsultAccessComponent


class ApiProcess:
    @staticmethod
    def list_all_process() -> list:
        return ConsultAccessComponent.all_info_run()

    @staticmethod
    def data_by_id_process(id: str) -> dict:
        return ConsultAccessComponent.by_id_run(id)

    @staticmethod
    def data_by_cologne_process(cologne: str) -> list:
        return ConsultAccessComponent.by_cologne_run(cologne)

    @staticmethod
    def wifi_ordered_by_proximity_process(latitude: float, longitude: float) -> list:
        return ConsultAccessComponent.proximity_run(latitude, longitude)
