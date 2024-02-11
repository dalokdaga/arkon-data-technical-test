
from app.api.core.component.list_all_componet import AccessComponent


class ApiProcess:
    @staticmethod
    def list_all_process() -> dict:
        return AccessComponent.run()

    @staticmethod
    def data_by_id_process(id: str) -> dict:
        return AccessComponent.by_id_run(id)

    @staticmethod
    def data_by_cologne_process(cologne: str) -> dict:
        return  AccessComponent.by_cologne_run(cologne)

    @staticmethod
    def wifi_ordered_by_proximity_process(latitude: float, longitude: float) -> dict:
        return AccessComponent.proximity_run(latitude, longitude)