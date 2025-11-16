import os
from flask import Flask, request, jsonify
from discord_interactions import verify_key_decorator

from handlers.gameserver_handler import get_gameserver_configurations, is_requested_server_currently_running
from structures import NewInteractionType as InteractionType, ServerActionInfo
from handlers.interaction_handler import handle_slash_command_request, handle_autocompletion_request

client_public_key = os.getenv('CLIENT_PUBLIC_KEY')
app = Flask('server-starter')


@app.route('/interactions', methods=['POST'])
@verify_key_decorator(client_public_key)
def interactions():
    body = request.json
    response = None

    if body['type'] == InteractionType.APPLICATION_COMMAND:
        response = handle_slash_command_request(body)
    elif body['type'] == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE:
        response = handle_autocompletion_request(body['data'])

    print(f'generated response body: {response.json}')
    return response


@app.route('/health', methods=['GET'])
def test():
    password = os.getenv('PASS')

    server_statuses = list()
    for gameserver_config in get_gameserver_configurations():
        server_status = dict()
        # spaghetti code yayyyyy i gotta refactor this stupid thing
        server_status[gameserver_config.name] \
            = is_requested_server_currently_running(gameserver_config, password, ServerActionInfo(gameserver_config.name, None, None))
        server_statuses.insert(server_status)

    return jsonify({'status': 'UP', 'version': '1.3', 'gameservers': server_statuses})
