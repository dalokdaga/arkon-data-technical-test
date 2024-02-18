import re
import json
from decouple import config


def open_text(path):
    ''' Method to open text files '''       
    with open(path, "r") as file:        
        text = file.read()
    return text


def open_json(path):
    ''' Method to open json files '''
    with open(path, 'r') as file:
        json_str = file.read()
    json_str = replace_env_variables(json_str)    
    return json.loads(json_str)


def replace_env_variables(json_str):
    ''' Method to replace environment variables in a str '''
    env_variables = re.findall(r'\${(\w+)}', json_str)
    for env_var in env_variables:
        value = config(env_var, None)
        if value:
            json_str = json_str.replace(f"${{{env_var}}}", value)
    return json_str
