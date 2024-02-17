from app.api.core.process import ApiProcess


class ApiHandler:
    @staticmethod
    def list_all_handler(**kwargs) -> dict:
        return ApiProcess.list_all_process(**kwargs)

    @staticmethod
    def data_by_id_handler(**kwargs) -> dict:
        return ApiProcess.data_by_id_process(**kwargs)

    @staticmethod
    def data_by_colony_handler(**kwargs) -> dict:
        return ApiProcess.data_by_colony_process(**kwargs)

    @staticmethod
    def wifi_ordered_by_proximity_handler(**kwargs) -> list:
        return ApiProcess.wifi_ordered_by_proximity_process(**kwargs)
