from app.core.common.utilities import open_text
from config.db.factory_db import FactoryDB

PATH_QUERYS = "app/api/core/querys/"


class ConsultAccessComponent:
    @staticmethod
    def all_info_run() -> list:
        database = FactoryDB.set_database()
        data = database.execute_query(open_text(f"{PATH_QUERYS}all_access.sql"))
        df_json = data.to_dict(orient='records')        
        return df_json

    @staticmethod
    def by_cologne_run(cologne: str) -> list:
        database = FactoryDB.set_database()
        data = database.execute_query(open_text(f"{PATH_QUERYS}by_cologne.sql"), (f"%{cologne}%"))
        df_json = data.to_dict(orient='records')        
        return df_json

    @staticmethod
    def by_id_run(id: str) -> dict:
        database = FactoryDB.set_database()
        data = database.execute_query(open_text(f"{PATH_QUERYS}by_id.sql"), (f"{id}"))
        df_json = data.to_dict(orient='records')
        if len(df_json) > 0:
            df_json = df_json[0]
        return {"data_one": df_json}

    @staticmethod
    def proximity_run(latitude: float, longitude: float) -> list:
        database = FactoryDB.set_database()
        data = database.execute_query(open_text(f"{PATH_QUERYS}proximity.sql"), (latitude, longitude, latitude))
        df_json = data.to_dict(orient='records')        
        return df_json
