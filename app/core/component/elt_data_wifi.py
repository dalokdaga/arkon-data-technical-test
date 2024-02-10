import pandas as pd
from app.core.constans import DB_PATH, FILE_PATH
from app.core.component.base_component import BaseComponent
from config.database_manager import DatabaseManager


class EtlDataWifi(BaseComponent):
    def __init__(self, file_name: str) -> None:
        self.__file_name = file_name
        self.run()

    def extraction(self) -> None:
        self.__data_frame = pd.read_csv(f'{FILE_PATH}/{self.__file_name}')

    def transformation(self) -> None:
        self.__colonies = self.set_colonies()

        # Suponiendo que tienes los DataFrames 'colonias' y 'registros'

        # Combinar los DataFrames 'registros' y 'colonias' basándote en las columnas 'colonia' y 'alcaldia'
        merge = self.__data_frame.merge(
            self.__colonies[['id', 'colonia', 'alcaldia']], on=['colonia', 'alcaldia'], how='left')

        # Renombrar la columna 'id' resultante a 'id_colonia'
        merge.rename(columns={'id_y': 'id_colonia'}, inplace=True)
        merge.rename(columns={'id_x': 'id'}, inplace=True)

        self.__data_frame = merge[['id', 'id_colonia', 'programa', 'fecha_instalacion', 'latitud', 'longitud']]

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
        database = DatabaseManager(f'{DB_PATH}/database.db')
        # conn = sqlite3.connect(f'{DB_PATH}/database.db')
        # Guarda el DataFrame en la base de datos SQLite
        database.save_data(self.__data_frame, 'registros_wifi')
        database.save_data(self.__colonies, 'colonies')

        database.disconnect()
