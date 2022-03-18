import os
from interaction_listener import app
from utils.command_creator import create_application_guild_commands
from argparse import ArgumentParser

parser = ArgumentParser(description='Bridge application to start/stop game servers with Discord app commands')
parser.add_argument('--create_commands', metavar='guild_id', type=str, required=False, help='do not run flask '
                                                                                            'application, '
                                                                                            'creates guild commands '
                                                                                            'instead')

args = parser.parse_args()
client_public_key = os.getenv('CLIENT_PUBLIC_KEY')
client_id = os.getenv('CLIENT_ID')  # also APP_ID
client_secret = os.getenv('CLIENT_SECRET')


if client_public_key and client_id:
    if args.create_commands:
        print(f'Creating commands for guild with id {args.create_commands}')
        create_application_guild_commands(client_id, client_secret, args.create_commands)
    else:
        print(f'Starting flask application')
        app.run()
else:
    print('client public key and app id must set as environment variables for normal operation')
    exit(1)
