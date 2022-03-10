from discord_interactions import InteractionType, InteractionResponseType


class Choice:
    def __init__(self, value):
        self.name = value
        self.value = value


class NewInteractionType(InteractionType):
    """Discord you massive dickheads make a god damn release of the library"""
    APPLICATION_COMMAND_AUTOCOMPLETE = 4


class NewInteractionResponseType(InteractionResponseType):
    """Discord you massive dickheads make a god damn release of the library"""
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
