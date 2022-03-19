import os
from flask import Flask, request
from discord_interactions import verify_key_decorator
from structures import NewInteractionType as InteractionType, ServerActionInfo, ActionType
from handlers.interaction_handler import handle_slash_command_request, handle_autocompletion_request
from threading import Thread
from handlers.gameserver_handler import perform_action

client_public_key = os.getenv('CLIENT_PUBLIC_KEY')
app = Flask('server-starter')


@app.route('/start', methods=['GET'])
def start_server():
    args = request.args.to_dict()
    server_name = args.get('name')
    startup_info = ServerActionInfo(server_name, ActionType.START, None)
    thread = Thread(target=perform_action, args=(startup_info,))
    thread.start()
    return 'server thread initiated, pray that it fucking works mate'


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

