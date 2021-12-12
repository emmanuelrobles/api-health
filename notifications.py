import json
from typing import List

import requests

from models import NewApiStatusAction, ApiStatusChangeAction


def teams_build_new_api_payload(data_list: List[NewApiStatusAction]) -> dict:
    api_status_text = ""
    for data in data_list:
        api_status_text += f'- {data.api.url} is **{data.status}**\r'

    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.0",
                    "body": [{
                        "type": "TextBlock",
                        "text": "Current api status"
                    }, {
                        "type": "TextBlock",
                        "text": api_status_text
                    }]
                }
            }
        ]
    }

    return payload


def teams_build_api_state_change_payload(data_list: List[ApiStatusChangeAction]) -> dict:
    api_status_text = ""
    for data in data_list:
        api_status_text += f'- {data.api.url} is **{data.status}**\r'

    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.0",
                    "body": [{
                        "type": "TextBlock",
                        "text": "Api state change detected"
                    }, {
                        "type": "TextBlock",
                        "text": api_status_text
                    }]
                }
            }
        ]
    }

    return payload


def notify_request(payload: dict, url: str):
    headers = {
        'Content-Type': 'application/json'
    }

    requests.post(url, headers=headers, data=json.dumps(payload))
