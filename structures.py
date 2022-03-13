import os
from discord_interactions import InteractionType, InteractionResponseType

DISCORD_API_ENDPOINT = 'https://discord.com/api/v8'


class Choice:
    def __init__(self, value):
        self.name = value
        self.value = value


class ActionType:
    NONE = ''
    START = 'start'
    STATUS = 'status'
    STOP = 'stop'


class ServerActionInfo:
    """Defines the name of the server to perform an action to, and contains
    its corresponding interaction token to send a response to discord after said action"""

    def __init__(self, name, action_type, interaction_token):
        self.name = name
        self.action_type = action_type
        self.interaction_token = interaction_token

    def get_followup_message_endpoint(self):
        return f'{self.get_new_followup_message_endpoint()}/messages/@original'

    def get_new_followup_message_endpoint(self):
        app_id = os.getenv('CLIENT_ID')
        return f'{DISCORD_API_ENDPOINT}/webhooks/{app_id}/{self.interaction_token}?wait=true'


class NewInteractionType(InteractionType):
    """Discord you massive dickheads make a god damn release of the library"""
    APPLICATION_COMMAND_AUTOCOMPLETE = 4


class NewInteractionResponseType(InteractionResponseType):
    """Discord you massive dickheads make a god damn release of the library"""
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
