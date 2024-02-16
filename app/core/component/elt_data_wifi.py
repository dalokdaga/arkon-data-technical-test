import requests
import pandas as pd
from io import StringIO
from app.core.exceptions import ExtractionErrorException, LoadErrorException, TransformationErrorException
from config.db.factory_db import FactoryDB
import config.enviroment as env
from app.core.component.base_component import BaseComponent


class EtlDataWifi(BaseComponent):
    def __init__(self, base_date: str=None) -> None:
        self.__base_date = base_date
        self.run()

    def extraction(self, ) -> None:
        try:
            url = env.URL_BASE.format(BASE_DATE=self.__base_date)
            response = requests.get(url)
            if response.status_code != 200:
                raise ExtractionErrorException(f"Failed to download CSV file. Status Code: {response.status_code}")
            csv_content = StringIO(response.text)
            self.__data_frame = pd.read_csv(csv_content)           
        except Exception as e:
            raise ExtractionErrorException(f"Extraction failed: {str(e)}")

    def transformation(self) -> None:
        try:
            self.__colonies = self.set_colonies()

            # Eliminar todas las comas excepto la primera y luego reemplazar la primera coma decimal con un punto
            # Eliminar todas las comas excepto la primera y luego reemplazar la primera coma decimal con un punto
            self.__data_frame['longitud'] = self.__data_frame['longitud'].apply(lambda x: x.replace(' ', ''))
            self.__data_frame['longitud'] = self.__data_frame['longitud'].apply(lambda x: x.replace(',', ''))
            self.__data_frame['longitud'] = self.__data_frame['longitud'].apply(lambda x: x.replace('.', ''))
            # Suponiendo que la columna de la longitud tiene el formato '-9907624200'
            self.__data_frame['longitud'] = self.__data_frame['longitud'].apply(lambda x: f"{x[:3]}.{x[3:6]}{x[6:]}")

            self.__data_frame['longitud'] = self.__data_frame['longitud'].astype(float)
            self.__data_frame['latitud'] = self.__data_frame['latitud'].astype(float)
            # Suponiendo que tienes los DataFrames 'colonias' y 'registros'

            # Combinar los DataFrames 'registros' y 'colonias' basándote en las columnas 'colonia' y 'alcaldia'
            merge = self.__data_frame.merge(
                self.__colonies[['id', 'colonia', 'alcaldia']], on=['colonia', 'alcaldia'], how='left')

            # Renombrar la columna 'id' resultante a 'id_colonia'
            merge.rename(columns={'id_y': 'id_colonia'}, inplace=True)
            merge.rename(columns={'id_x': 'id'}, inplace=True)

            self.__data_frame = merge[['id', 'id_colonia', 'programa', 'fecha_instalacion', 'latitud', 'longitud']]
        except Exception as e:
            raise TransformationErrorException(f"Transformation failed: {str(e)}")

    def set_colonies(self) -> pd.DataFrame:
        # Eliminar los registros que tienen valores erróneos o faltantes en la columna 'colonia'
        self.__data_frame = self.__data_frame[self.__data_frame['colonia'] != '#¡REF!']

        # Restablecer los índices después de eliminar las filas
        self.__data_frame.reset_index(drop=True, inplace=True)

        self.__data_frame['colonia'] = self.__data_frame['colonia'].astype(str)
        self.__data_frame['alcaldia'] = self.__data_frame['alcaldia'].astype(str)  

        self.__data_frame.reset_index(drop=False, inplace=True)

        self.__data_frame['colonia'] = self.__data_frame['colonia'].apply(self.normalize_text)
        self.__data_frame['alcaldia'] = self.__data_frame['alcaldia'].apply(self.normalize_text)

        # Concatenar el nombre de la colonia y de la alcaldía
        self.__data_frame['colonia_alcaldia'] = self.__data_frame['colonia'] + '_' + self.__data_frame['alcaldia']

        # Generar un hash único para cada combinación única de colonia y alcaldía
        self.__data_frame['hash_colonia'] = self.__data_frame['colonia_alcaldia'].apply(hash)

        # Eliminar la columna temporal 'colonia_alcaldia'
        self.__data_frame.drop(columns=['colonia_alcaldia'], inplace=True)

        # Agrupar por colonia y alcaldía y obtener combinaciones únicas
        colonies = self.__data_frame.groupby(['colonia', 'alcaldia']).agg({'hash_colonia': 'first'}).reset_index()

        # Reiniciar el índice y sumar 1 para obtener el ID de colonia
        colonies.reset_index(drop=True, inplace=True)
        colonies['id'] = colonies.index + 1

        # Reorganizar el DataFrame para que la columna 'id' esté al principio
        colonies = colonies[['id', 'colonia', 'alcaldia']]                
        return colonies

    def load(self) -> None:
        try:       
            database = FactoryDB.set_database()
            database.save_data(self.__data_frame, 'registros_wifi')
            database.save_data(self.__colonies, 'colonies')

            database.disconnect()
        except Exception as e:
            raise LoadErrorException(f"Load failed: {str(e)}")
