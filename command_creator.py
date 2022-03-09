import requests

DISCORD_API_ENDPOINT = 'https://discord.com/api/v8'
CREATE_COMMAND_URL = '/applications/{0}/guilds/{1}/commands'
OAUTH_TOKEN_URL = '/oauth2/token'


def create_application_guild_commands(application_id, client_secret, guild_id):
    bearer_token = get_bearer_token(application_id, client_secret)

    if bearer_token:
        json = {        # replace with ingesting from json
            'name': 'test',
            'description': 'test creating application command without bot app',
            'type': '1'
        }

        headers = {
            'Authorization': f'Bearer {bearer_token}'
        }

        return requests.post(DISCORD_API_ENDPOINT + CREATE_COMMAND_URL.format(application_id, guild_id),
                             headers=headers, json=json)

    print('bearer token is empty, not making any command requests')
    return None


def get_bearer_token(client_id, client_secret):
    body = {
        'grant_type': 'client_credentials',
        'scope': 'applications.commands applications.commands.update'
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
