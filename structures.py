import os
from discord_interactions import InteractionType, InteractionResponseType
from utils.api_utils import DISCORD_API_ENDPOINT


class Choice:
    def __init__(self, value):
        self.name = value
        self.value = value


class ServerStartupInfo:
    def __init__(self, name, interaction_token):
        self.name = name
        self.interaction_token = interaction_token

    def get_followup_message_endpoint(self):
        return f'{self.get_new_followup_message_endpoint()}/messages/@original'

    def get_new_followup_message_endpoint(self):
        app_id = os.getenv('CLIENT_ID')
        return f'{DISCORD_API_ENDPOINT}/webhooks/{app_id}/{self.interaction_token}'


class NewInteractionType(InteractionType):
    """Discord you massive dickheads make a god damn release of the library"""
    APPLICATION_COMMAND_AUTOCOMPLETE = 4


class NewInteractionResponseType(InteractionResponseType):
    """Discord you massive dickheads make a god damn release of the library"""
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
