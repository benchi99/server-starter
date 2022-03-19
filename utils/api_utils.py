import requests
from structures import ServerActionInfo


def send_followup_response(text_content, action_info: ServerActionInfo, ephemeral=False):
    if action_info.interaction_token != '' or None:
        json_data = {
            'content': text_content
        }

        if ephemeral:
            json_data['flags'] = 64

        url = action_info.get_new_followup_message_endpoint()

        r = requests.post(url, json=json_data)

        if not r.ok:
            print(f'fucking idk discord is pretty sad they said {r.content}')
        else:
            print('responded to deferred interaction properly mate sick 😎')
    else:
        print('no interaction token present - not sending response to discord')
