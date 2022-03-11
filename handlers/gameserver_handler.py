from utils.json_load_utils import load_json_data_from_path


def get_gameserver_names():
    for gameserver_config in load_json_data_from_path('./resources/serverconfigs'):
        yield gameserver_config['name']


def run_gameserver():
    pass
