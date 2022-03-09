import os
from flask import Flask, request, jsonify
from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType

client_public_key = os.getenv('CLIENT_PUBLIC_KEY')
app = Flask('server-starter')


@app.route('/interactions', methods=['POST'])
@verify_key_decorator(client_public_key)
def interactions():
    print('yo thats discord touching me OwO')
    if request.json['type'] == InteractionType.APPLICATION_COMMAND:
        return jsonify({
            'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            'data': {
                'content': 'I have been reached omg omg please implement command handling you moron'
            }
        })


def start_flask_application():
    app.run()
