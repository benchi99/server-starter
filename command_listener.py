import os
from flask import Flask, request
from discord_interactions import verify_key_decorator
from structures import NewInteractionType as InteractionType
from command_handler import handle_slash_command_request, handle_autocompletion_request

client_public_key = os.getenv('CLIENT_PUBLIC_KEY')
app = Flask('server-starter')


@app.route('/interactions', methods=['POST'])
@verify_key_decorator(client_public_key)
def interactions():
    body = request.json
    if body['type'] == InteractionType.APPLICATION_COMMAND:
        return handle_slash_command_request(body['data'])
    elif body['type'] == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE:
        handle_autocompletion_request(body['data'])


def start_flask_application():
    app.run()
