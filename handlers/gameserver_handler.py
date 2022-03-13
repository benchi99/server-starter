from utils.json_load_utils import load_json_data_from_path
import subprocess
from structures import ServerActionInfo, ActionType
from utils.api_utils import send_followup_response


def get_gameserver_configurations():
    for gameserver_config in load_json_data_from_path('./resources/serverconfigs'):
        yield gameserver_config


def get_gameserver_configuration_by_name(name):
    for gameserver_config in get_gameserver_configurations():
        if gameserver_config['name'] == name:
            return gameserver_config

    return None


def perform_action(action_info: ServerActionInfo):
    action_result_message = None

    for gameserver_config in get_gameserver_configurations():
        if gameserver_config['name'] == action_info.name:
            user = gameserver_config['user']
            desired_script = gameserver_config[action_info.action_type]['script']
            # command = f' echo {user["password"]} | sudo -S -u {user["username"]} \'{desired_script}\''
            command = 'whoami'

            action_command = subprocess.run(command, text=True, capture_output=True)
            try:
                action_command.check_returncode()
                print(f'hey sick the command ran just fine and it printed {action_command.stdout}')
                action_result_message = get_success_message_for_action(action_info.action_type, action_info.name)
            except subprocess.CalledProcessError as e:
                print('fuck the script failed to run dude what the hell')
                action_result_message = get_failure_message_for_action(action_info.action_type, action_info.name, e)

    send_followup_response(action_result_message, action_info)


def get_success_message_for_action(action: ActionType, name: str) -> str:
    if action is ActionType.START:
        return f'Game server {name} has been initiated, it may take some time to be up'
    elif action is ActionType.STOP:
        return f'Game server {name} has stopped successfully'


def get_failure_message_for_action(action: ActionType, name: str, e: subprocess.CalledProcessError) -> str:
    if action is ActionType.START:
        return f'The startup script for {name} exited with a non-zero code (code {e.returncode}).' \
               f' This was the console output: ```{e.stdout}```'
    elif action is ActionType.STATUS:
        return f'The script to fetch the status for {name} exited with a non-zero code (code {e.returncode}). ' \
            f' This was the console output: ```{e.stdout}```'
    elif action is ActionType.STOP:
        return f'The script for stopping {name} exited with a non-zero code (code {e.returncode}).' \
            f' This was the console output: ```{e.stdout}```'
