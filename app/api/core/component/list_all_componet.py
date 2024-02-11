from config.db.factory_db import FactoryDB


class AccessComponent:
    @staticmethod
    def all_info_run() -> list:
        database = FactoryDB.set_database()
        data = database.execute_query("""
            SELECT 
                rw.id,
                rw.programa,
                rw.fecha_instalacion,
                rw.latitud,
                rw.longitud,
                c.colonia,
                c.alcaldia 
            FROM arkon_test.registros_wifi rw 
            left join arkon_test.colonies c on rw.id_colonia = c.id 
        """)
        df_json = data.to_dict(orient='records')
        print(df_json)
        return df_json

    @staticmethod
    def by_cologne_run(cologne: str) -> list:
        database = FactoryDB.set_database()
        data = database.execute_query("""
        SELECT 
            rw.id,
            rw.programa,
            rw.fecha_instalacion,
            rw.latitud,
            rw.longitud,
            c.colonia,
            c.alcaldia 
        FROM arkon_test.registros_wifi rw 
        left join arkon_test.colonies c on rw.id_colonia = c.id 
        where c.colonia  LIKE '%s'
        """, (f"%{cologne}%"))
        df_json = data.to_dict(orient='records')
        print(df_json)
        return df_json

    @staticmethod
    def by_id_run(id: str) -> dict:
        database = FactoryDB.set_database()
        data = database.execute_query("""
        SELECT 
            rw.id,
            rw.programa,
            rw.fecha_instalacion,
            rw.latitud,
            rw.longitud,
            c.colonia,
            c.alcaldia 
        FROM arkon_test.registros_wifi rw 
        left join arkon_test.colonies c on rw.id_colonia = c.id 
        where rw.id  LIKE '%s'
        """, (f"%{id}%"))
        df_json = data.to_dict(orient='records')
        print(df_json)
        if len(df_json) > 0:
            df_json = df_json[0]
        return {"data_one": df_json}

    @staticmethod
    def proximity_run(latitude: float, longitude: float) -> list:
        database = FactoryDB.set_database()
        data = database.execute_query("""
        SELECT
            rw.id,
            rw.programa,
            rw.fecha_instalacion,
            rw.latitud,
            rw.longitud,
            c.colonia,
            c.alcaldia,
            (6371 * acos(cos(radians(%s)) * cos(radians(rw.latitud)) *
            cos(radians(rw.longitud) - radians(%s)) +
            sin(radians(%s)) * sin(radians(rw.latitud)))) AS distancia
        FROM
            arkon_test.registros_wifi rw
        left join arkon_test.colonies c on
            rw.id_colonia = c.id
        ORDER BY
            distancia
        """, (latitude, longitude, latitude))
        df_json = data.to_dict(orient='records')
        print(df_json)
        return df_json
