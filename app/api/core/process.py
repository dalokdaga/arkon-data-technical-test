
class ApiProcess:
    @staticmethod
    def list_all_process() -> dict:
        return {"access_points": []}

    @staticmethod
    def data_by_id_process(id: str) -> dict:
        return {
            "data_one": {}
        }

    @staticmethod
    def data_by_cologne_process(cologne: str) -> dict:
        return {
            "access_points": [cologne]
        }

    @staticmethod
    def wifi_ordered_by_proximity_process(latitude: float, longitude: float) -> dict:
        return {
            "access_points": [
                {
                    "list_by_proximity": {
                        "latitude": latitude,
                        "longitude": longitude
                    }
                }
            ]
        }