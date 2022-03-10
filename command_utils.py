from structures import NewInteractionResponseType as InteractionResponseType
from discord_interactions import InteractionResponseFlags
from flask import jsonify
import json


def respond_with_message(text_content):
    """Creates a JSON response as a text message in a channel"""
    return jsonify({
        'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        'data': {
            'content': text_content
        }
    })


def respond_with_ephemeral_message(text_content):
    """Creates a JSON response as an ephemeral text message in channel"""
    return jsonify({
        'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        'data': {
            'content': text_content,
            'flags': InteractionResponseFlags.EPHEMERAL
        }
    })


def respond_with_autocomplete_suggestions(choices):
    """Creates a JSON response for autocomplete suggestions"""
    return jsonify({
        'type': InteractionResponseType.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT,
        'data': {
            'choices': json.dumps(choices)
        }
    })
