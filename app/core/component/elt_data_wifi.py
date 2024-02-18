import requests
import pandas as pd
from io import StringIO
from app.core.exceptions import ExtractionErrorException, LoadErrorException, TransformationErrorException
from config.db.factory_db import FactoryDB
import config.enviroment as env
from app.core.component.base_component import BaseComponent


class EtlDataWifi(BaseComponent):
    ''' ETL in charge of extracting, transforming and loading information '''
    def __init__(self, base_date: str = None) -> None:
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

            # Convert the 'latitude' and 'longitude' columns to string type
            self.__data_frame['latitud'] = self.__data_frame['latitud'].astype(str)
            self.__data_frame['longitud'] = self.__data_frame['longitud'].astype(str)

            # Clear and transform the 'latitude' column
            self.__data_frame['latitud'] = self.__data_frame['latitud'].apply(self.clean_longitud)                    
            self.__data_frame['latitud'] = self.__data_frame['latitud'].apply(self.transform_longitud)

            # Clear and transform the 'length' column
            self.__data_frame['longitud'] = self.__data_frame['longitud'].apply(self.clean_longitud)                        
            self.__data_frame['longitud'] = self.__data_frame['longitud'].apply(self.transform_longitud)

            # Convert the 'latitude' and 'longitude' columns to float type
            self.__data_frame['longitud'] = self.__data_frame['longitud'].astype(float)
            self.__data_frame['latitud'] = self.__data_frame['latitud'].astype(float)

            # Perform the union of the DataFrames 'data_frame' and 'colonies'
            merge = self.__data_frame.merge(
                self.__colonies[['id', 'colonia', 'alcaldia']], on=['colonia', 'alcaldia'], how='left')
            
            # Rename columns
            merge.rename(columns={'id_y': 'id_colonia'}, inplace=True)
            merge.rename(columns={'id_x': 'id'}, inplace=True)

            self.__data_frame = merge[['id', 'id_colonia', 'programa', 'fecha_instalacion', 'latitud', 'longitud']]
        except Exception as e:
            raise TransformationErrorException(f"Transformation failed: {str(e)}")

    def clean_longitud(self, x):
        ''' Method to clear the 'length' column '''
        x = x.replace(' ', '')
        x = x.replace(',', '')
        x = x.replace('.', '')
        return x

    def transform_longitud(self, x):
        ''' Method to transform coordinate '''
        if x.startswith('-'):
            return f"{x[:3]}.{x[3:6]}{x[6:]}"
        else:
            return f"{x[:2]}.{x[3:6]}{x[6:]}"

    def set_colonies(self) -> pd.DataFrame:
        # Delete records that have wrong or missing values ​​in the 'colony' column
        self.__data_frame = self.__data_frame[self.__data_frame['colonia'] != '#¡REF!']

        # Reset indexes after deleting rows
        self.__data_frame.reset_index(drop=True, inplace=True)

        self.__data_frame['colonia'] = self.__data_frame['colonia'].astype(str)
        self.__data_frame['alcaldia'] = self.__data_frame['alcaldia'].astype(str)  

        self.__data_frame.reset_index(drop=False, inplace=True)

        self.__data_frame['colonia'] = self.__data_frame['colonia'].apply(self.normalize_text)
        self.__data_frame['alcaldia'] = self.__data_frame['alcaldia'].apply(self.normalize_text)

        # Concatenate the name of the neighborhood and the mayor's office
        self.__data_frame['colonia_alcaldia'] = self.__data_frame['colonia'] + '_' + self.__data_frame['alcaldia']

        # Generate a unique hash for each unique neighborhood and mayoralty combination
        self.__data_frame['hash_colonia'] = self.__data_frame['colonia_alcaldia'].apply(hash)

        # Delete the temporary column 'colonia_alcaldia'
        self.__data_frame.drop(columns=['colonia_alcaldia'], inplace=True)

        # Group by neighborhood and municipality and obtain unique combinations
        colonies = self.__data_frame.groupby(['colonia', 'alcaldia']).agg({'hash_colonia': 'first'}).reset_index()

        # Reset the index and add 1 to get the colony ID
        colonies.reset_index(drop=True, inplace=True)
        colonies['id'] = colonies.index + 1

        # Rearrange the DataFrame so that the 'id' column is at the beginning
        colonies = colonies[['id', 'colonia', 'alcaldia']]                
        return colonies

    def load(self) -> None:
        try:       
            database = FactoryDB.set_database()
            database.save_data(self.__data_frame, 'wifi_logs')
            database.save_data(self.__colonies, 'colonies')

            database.disconnect()
        except Exception as e:
            raise LoadErrorException(f"Load failed: {str(e)}")
