from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from app.api.core.exceptions import DatabaseErrorException, NotFoundException
from app.api.core.helper import build_combined_records
from app.api.core.models import Colony, WifiRecord
from app.api.core.paginator import PaginationInfo
from app.core.common.utilities import open_json
import config.enviroment as env


# Configure the connection to the database and create the session
rule_db = open_json(env.PATH_RULE_DB)[env.TYPE_DB]
connection_uri = rule_db['connection_string']
engine = create_engine(connection_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_wifi_record_by_id(id_wifi):
    ''' Query the WifiRecord record for its identifier using session '''
    try:
        session = SessionLocal()

        wifi_record = session.query(WifiRecord).filter_by(id=id_wifi).first()
        if not wifi_record:
            raise NotFoundException(f"Record with id {id_wifi} not found")
        record = wifi_record.as_dict()
        colony = wifi_record.colony       
        record.update(colony.as_dict())
        return record        
    except Exception as e:
        raise DatabaseErrorException(f"{get_wifi_record_by_id.__name__}-{str(e)}")
    finally:
        session.close()


def search_wifi_records_like(colony_name, offset: int, limit: int):
    '''  Perform the query filtering by the name of the colony and applying offset and limit '''
    try:
        session = SessionLocal()

        total_items = (
            session.query(WifiRecord)
            .join(WifiRecord.colony)
            .filter(Colony.colonia.like(f'%{colony_name}%'))
            .count()
        )

        wifi_records = (
            session.query(WifiRecord, Colony)
            .join(WifiRecord.colony)
            .filter(Colony.colonia.like(f'%{colony_name}%'))
            .offset(offset)
            .limit(limit)
            .all()
        )

        combined_records = build_combined_records(wifi_records)

        pagination_info = PaginationInfo(total_items, limit, offset)

        return {"access_points": combined_records, "pagination_info": pagination_info.as_dict()}
    except Exception as e:
        raise DatabaseErrorException(f"{search_wifi_records_like.__name__}-{str(e)}")
    finally:
        session.close()


def get_all_wifi_records(offset: int, limit: int):
    ''' Check all records and applying offset and limit'''
    try:
        session = SessionLocal()        

        total_items = session.query(WifiRecord).count()

        wifi_records = (
            session.query(WifiRecord, Colony)
            .join(WifiRecord.colony)
            .offset(offset)
            .limit(limit)
            .all()
        )

        combined_records = build_combined_records(wifi_records)

        pagination_info = PaginationInfo(total_items, limit, offset)

        return {"access_points": combined_records, "pagination_info": pagination_info.as_dict()}
    except Exception as e:
        raise DatabaseErrorException(f"{search_wifi_records_like.__name__}-{str(e)}")
    finally:
        session.close()


def get_all_wifi_proximity(lat: float, lon: float, offset: int, limit: int,):
    ''' Gets the records sorted by proximity to the entered coordinates. '''
    try:
        session = SessionLocal()

        total_items = session.query(WifiRecord).count()

        wifi_records = (
            session.query(
                WifiRecord,
                Colony,
                (
                    func.acos(
                        func.cos(
                            func.radians(lat)) * func.cos(func.radians(WifiRecord.latitud)) * func.cos(
                                func.radians(WifiRecord.longitud) - func.radians(lon)) + func.sin(func.radians(lat)
                            ) * func.sin(func.radians(WifiRecord.latitud))
                    ) * 6371  # Calculate the distance in kilometers
                ).label("distance")
            ) 
            .join(WifiRecord.colony)  # Perform a join with the Colony table
            .order_by("distance")  # Sort by calculated distance
            .offset(offset)
            .limit(limit)
            .all()
        )        
        # Build a list of dictionaries by combining WifiRecord, Colony and distance data
        combined_records = []
        for wifi_record, colony, distance in wifi_records:
            record_dict = wifi_record.as_dict() 
            colony_dict = colony.as_dict()
            record_dict.update(colony_dict)
            record_dict["distancia"] = distance
            combined_records.append(record_dict)

        pagination_info = PaginationInfo(total_items, limit, offset)

        return {"access_points": combined_records, "pagination_info": pagination_info.as_dict()}
    except Exception as e:
        raise DatabaseErrorException(f"{search_wifi_records_like.__name__}-{str(e)}")
    finally:
        session.close()  
