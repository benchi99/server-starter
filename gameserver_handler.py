from json_load_utils import load_json_data_from_path


def get_gameserver_names():
    for gameserver_config in load_json_data_from_path('./serverconfigs'):
        yield gameserver_config['name']
