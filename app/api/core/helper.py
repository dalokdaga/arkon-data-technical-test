

from app.api.core.models import WifiRecord


def build_combined_records(wifi_records: WifiRecord):
    ''' Build a list of dictionaries by combining WifiRecord and Colony data '''
    combined_records = []
    for wifi_record, colony in wifi_records:
        record_dict = wifi_record.as_dict()
        colony_dict = colony.as_dict()
        record_dict.update(colony_dict)
        combined_records.append(record_dict)
    return combined_records
