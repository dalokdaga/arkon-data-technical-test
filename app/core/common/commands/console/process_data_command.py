from app.core.component.elt_data_wifi import EtlDataWifi
import config.enviroment as env


class ProcessData:

    @staticmethod
    def process_data(file_date: str):        
        return EtlDataWifi(f'{file_date}-{env.FILE_NAME}')
