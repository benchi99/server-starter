import os
from flask import Flask, request
from discord_interactions import verify_key_decorator
from structures import NewInteractionType as InteractionType
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
