import re
import json
from decouple import config


def open_json(path):
    with open(path, 'r') as file:
        json_str = file.read()
    json_str = replace_env_variables(json_str)
    print(json_str)
    return json.loads(json_str)


def replace_env_variables(json_str):
    env_variables = re.findall(r'\${(\w+)}', json_str)
    for env_var in env_variables:
        value = config(env_var, None)
        if value:
            json_str = json_str.replace(f"${{{env_var}}}", value)
    return json_str
