import os
import json


def load_json_data_from_path(path):
    """Returns generator of all json files within a directory"""
    for root, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            if file_name.endswith('.json'):
                file = open(f'{path}/{file_name}')
                yield json.load(file)
