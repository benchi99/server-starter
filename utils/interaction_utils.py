from structures import NewInteractionResponseType as InteractionResponseType
from discord_interactions import InteractionResponseFlags
from flask import jsonify


def respond_with_message(text_content):
    """Creates a JSON response as a text message in a channel"""
    return jsonify({
        'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        'data': {
            'content': text_content
        }
    })


def respond_with_deferred_message():
    """Creates a JSON response that ACKs the interaction, to respond afterwards"""
    return jsonify({
        'type': InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE
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
            'choices': choices
        }
    })
