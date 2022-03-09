import requests
import os
import json

DISCORD_API_ENDPOINT = 'https://discord.com/api/v8'
CREATE_COMMAND_URL = '/applications/{0}/guilds/{1}/commands'
OAUTH_TOKEN_URL = '/oauth2/token'


def create_application_guild_commands(application_id, client_secret, guild_id):
    bearer_token = get_bearer_token(application_id, client_secret)

    if bearer_token:
        headers = {
            'Authorization': f'Bearer {bearer_token}'
        }

        url = f'{DISCORD_API_ENDPOINT}{CREATE_COMMAND_URL.format(application_id, guild_id)}'

        for command_definition in get_command_definitions():
            print(f'Attempting to create command {command_definition["name"]}')
            response = requests.post(url, headers=headers, json=command_definition)
            if response.ok:
                print(f'request result: status: {response.status_code}')
            else:
                print(f'request result: status: {response.status_code}, body: {response.text}')
    else:
        print('bearer token is empty, not making any command requests')


def get_bearer_token(client_id, client_secret):
    body = {
        'grant_type': 'client_credentials',
        'scope': 'applications.commands.update'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    auth_response \
        = requests.post(f'{DISCORD_API_ENDPOINT}{OAUTH_TOKEN_URL}', data=body, headers=headers, auth=(client_id,
                                                                                                      client_secret))

    if auth_response.ok:
        return auth_response.json()['access_token']
    else:
        print(f'failed to get a bearer token response code {auth_response.status_code}, body: {auth_response.text}')
        return ''


def get_command_definitions():
    path = './commands'

    for root, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            if file_name.endswith('.json'):
                file = open(f'{path}/{file_name}')
                yield json.load(file)
