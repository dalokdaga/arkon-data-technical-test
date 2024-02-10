from app.core.component.elt_data_wifi import EtlDataWifi
from app.core.constans import FILE_NAME


class ProcessData:

    @staticmethod
    def process_data(file_date: str):        
        return EtlDataWifi(f'{file_date}-{FILE_NAME}')
