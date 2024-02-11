
from app.core.common.utilities import open_json
import config.enviroment as env
from importlib import import_module


class FactoryDB:
    @staticmethod
    def set_database():
        rule_db = open_json(env.PATH_RULE_DB)[env.TYPE_DB]
        module_db = import_module(f"config.db.drivers.{rule_db['driver']}.driver")
        return module_db.DriverDB(rule_db['connection_string'])

