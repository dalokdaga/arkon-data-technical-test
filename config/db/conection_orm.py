
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config.enviroment as env
from app.core.common.utilities import open_json

rule_db = open_json(env.PATH_RULE_DB)[env.TYPE_DB]

engine = create_engine(
    rule_db['connection_string'], connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
