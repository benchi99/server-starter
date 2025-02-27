import os
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
    password = os.getenv('PASS')

    if password is not None:
        result_message = None

        for gameserver_config in get_gameserver_configurations():
            if gameserver_config['name'] == action_info.name:
                result_message = execute_action(gameserver_config, password, action_info)
                break

        send_followup_response(result_message, action_info)
    else:
        print('password was not set - nothing was run')
        send_followup_response('No password for running servers has been set, nothing was executed', action_info)


def execute_action(gameserver_config, password, action_info: ServerActionInfo) -> str:
    if is_requested_server_under_maintenance(gameserver_config):
        print('requested server is currently set to under maintenance! please update config when maintenance is done')
        return 'Sorry! The server is under maintenance, and the server cannot be started at this time.'
    else:
        if can_requested_action_be_executed(gameserver_config, password, action_info):
            command = get_command_to_run(gameserver_config, password, action_info)

            action_command = subprocess.run(command, text=True, capture_output=True, shell=True)
            try:
                action_command.check_returncode()
                print(f'hey sick the command ran just fine and it printed {action_command.stdout}')
                return get_success_message_for_action(action_info.action_type, action_info.name)
            except subprocess.CalledProcessError as e:
                if e.returncode == 1:
                    if action_info.action_type != ActionType.STATUS:
                        print('fuck the script failed to run dude what the hell')
                        print(f'stdout: {e.stdout}')
                        print(f'stderr: {e.stderr}')
                    return get_fatal_failure_message_for_action(action_info.action_type, action_info.name, e)
                else:
                    print('something went wrong but the script might have gone thru')
                    return get_failure_message_for_action(action_info.action_type, action_info.name, e)
        else:
            server_status_message = 'running' if action_info.action_type == ActionType.START else 'stopped'
            print(f'Tried {server_status_message} game server {action_info.name} but its already in that state')
            return f'The action cannot be performed, the server is already {server_status_message}!'


def get_command_to_run(gameserver_config, password, action_info: ServerActionInfo) -> str:
    user = gameserver_config['user']
    desired_script = gameserver_config[action_info.action_type]['script']
    return f' echo \'{password}\' | sudo -S -u {user} {desired_script}'


def can_requested_action_be_executed(gameserver_config, password, action_info) -> bool:
    if action_info.action_type == ActionType.START:
        return not is_requested_server_currently_running(gameserver_config, password, action_info)
    elif action_info.action_type == ActionType.STATUS:
        return True  # checking for status should always be allowed
    elif action_info.action_type == ActionType.STOP:
        return is_requested_server_currently_running(gameserver_config, password, action_info)
    return False


def is_requested_server_under_maintenance(gameserver_config) -> bool:
    try:
        return gameserver_config['maintenance']
    except KeyError:
        return False


def is_requested_server_currently_running(gameserver_config, password, action_info) -> bool:
    # dummy copy, won't require interaction token since it won't be used to make requests to discord
    new_action_info = ServerActionInfo(name=action_info.name, action_type=ActionType.STATUS, interaction_token='')
    command = get_command_to_run(gameserver_config, password, new_action_info)
    status_command = subprocess.run(command, text=True, capture_output=True, shell=True)

    try:
        status_command.check_returncode()
        return True
    except subprocess.CalledProcessError:
        return False


def get_success_message_for_action(action: ActionType, name: str):
    if action == ActionType.START:
        return f'Game server {name} has been initiated, it may take some time to be up'
    elif action == ActionType.STATUS:
        return f'Server status of {name}: Server is running.'
    elif action == ActionType.STOP:
        return f'Game server {name} has stopped successfully'


def get_failure_message_for_action(action: ActionType, name: str, e: subprocess.CalledProcessError):
    if action == ActionType.START:
        return f'The startup script for {name} exited with a non-zero code (code {e.returncode}).' \
               f' This was the console output: ```{e.stdout + e.stderr}```'
    elif action == ActionType.STATUS:
        return f'The script to fetch the status for {name} exited with a non-zero code (code {e.returncode}). ' \
               f' This was the console output: ```{e.stdout + e.stderr}```'
    elif action == ActionType.STOP:
        return f'The script for stopping {name} exited with a non-zero code (code {e.returncode}).' \
               f' This was the console output: ```{e.stdout + e.stderr}```'


def get_fatal_failure_message_for_action(action: ActionType, name: str, e: subprocess.CalledProcessError):
    if action == ActionType.START:
        return f'The startup script for {name} ran into a fatal error and did not start up.' \
               f' This was the console output: ```{e.stdout + e.stderr}```'
    elif action == ActionType.STATUS:  # Return code 1 for status scripts means server is not running
        return f'Server status for {name}: Server is not running'
    elif action == ActionType.STOP:
        return f'The script for stopping {name} ran into a fatal error and did not stop.' \
               f' The server is most likely still running. This was the console output: ```{e.stdout + e.stderr}```'
