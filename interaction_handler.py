from gameserver_handler import get_gameserver_names
from interaction_utils import respond_with_autocomplete_suggestions, respond_with_message
from structures import Choice


def handle_start(server_name):
    print(f'starting {server_name}')
    return respond_with_message('started server')


def handle_status(server_name):
    print(f'checking status of {server_name}')
    return respond_with_message('server status')


def handle_stop(server_name):
    print(f'stopping {server_name}')
    return respond_with_message('stopped server')


handler_dict = {
    "start": handle_start,
    "status": handle_status,
    "stop": handle_stop
}


def handle_slash_command_request(command_data):
    for name in handler_dict:
        if command_data['name'] == name:
            server_name = command_data['options'][0]['value']
            return handler_dict[name](server_name)


def handle_autocompletion_request(autocomplete_data):
    partial_parameter_data = get_partial_value(autocomplete_data)
    print(f'currently inputted data: {partial_parameter_data}')
    choices = list()

    for gameserver_name in get_gameserver_names():
        if gameserver_name.startswith(partial_parameter_data):
            choices.append(Choice(gameserver_name).__dict__)

    print(f'current suggestions {choices}')

    return respond_with_autocomplete_suggestions(choices)


def get_partial_value(autocomplete_data) -> str:
    options = autocomplete_data['options']
    for option in options:
        if option['focused']:
            return option['value']
