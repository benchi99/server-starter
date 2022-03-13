from utils.interaction_utils \
    import respond_with_autocomplete_suggestions, respond_with_ephemeral_message, respond_with_deferred_message, \
    get_user_id_from_interaction
from structures import Choice, ServerActionInfo, ActionType
from threading import Thread
from handlers.gameserver_handler \
    import perform_action, get_gameserver_configurations, get_gameserver_configuration_by_name


def handle_start(server_name, interaction_data):
    if invoking_user_can_run_command(interaction_data, server_name, ActionType.START):
        print(f'starting {server_name}')
        startup_info = ServerActionInfo(server_name, ActionType.START, interaction_data['token'])
        thread = Thread(target=perform_action, args=(startup_info,))
        thread.start()
        return respond_with_deferred_message()
    else:
        respond_with_ephemeral_message('You do not have permission to run this command, sorry!')


def handle_status(server_name, interaction_data):
    print(f'checking status of {server_name}')
    return respond_with_ephemeral_message('server status')


def handle_stop(server_name, interaction_data):
    print(f'stopping {server_name}')
    return respond_with_ephemeral_message('stopped server')


handler_dict = {
    "start": handle_start,
    "status": handle_status,
    "stop": handle_stop
}


def handle_slash_command_request(interaction_data):
    data = interaction_data['data']

    for name in handler_dict:
        if data['name'] == name:
            server_name = data['options'][0]['value']
            return handler_dict[name](server_name, interaction_data)


def handle_autocompletion_request(autocomplete_data):
    partial_parameter_data = get_partial_value(autocomplete_data)
    print(f'currently inputted data: {partial_parameter_data}')
    choices = list()

    for gameserver_config in get_gameserver_configurations():
        if gameserver_config['name'].startswith(partial_parameter_data):
            choices.append(Choice(gameserver_config).__dict__)

    print(f'current suggestions {choices}')

    return respond_with_autocomplete_suggestions(choices)


def get_partial_value(autocomplete_data) -> str:
    options = autocomplete_data['options']
    for option in options:
        if option['focused']:
            return option['value']


def invoking_user_can_run_command(server_name, interaction_data, action_type):
    user_id = get_user_id_from_interaction(interaction_data)
    game_config = get_gameserver_configuration_by_name(server_name)

    if game_config is not None:
        allowed_users = game_config[action_type]['allowed_users_to_run_command']
        return True if user_id in allowed_users or allowed_users is None else False

    return False
