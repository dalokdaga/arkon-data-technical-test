from app.api.core.process import ApiProcess


class ApiHandler:
    @staticmethod
    def list_all_handler() -> list:
        return ApiProcess.list_all_process()

    @staticmethod
    def data_by_id_handler(**kwargs) -> dict:
        return ApiProcess.data_by_id_process(**kwargs)

    @staticmethod
    def data_by_cologne_handler(**kwargs) -> list:
        return ApiProcess.data_by_cologne_process(**kwargs)

    @staticmethod
    def wifi_ordered_by_proximity_handler(**kwargs) -> list:
        return ApiProcess.wifi_ordered_by_proximity_process(**kwargs)
