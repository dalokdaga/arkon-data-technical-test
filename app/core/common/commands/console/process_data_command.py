from app.core.component.elt_data_wifi import EtlDataWifi


class ProcessDataConsole:

    @staticmethod
    def process_data(file_date: str):        
        return EtlDataWifi(file_date)
