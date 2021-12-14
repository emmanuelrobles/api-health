from typing import Callable

import requests as requests

from actions import on_api_up, on_api_down
from models import Api, Action


def check_swagger(url: str) -> bool:
    swagger = url + "/swagger/index.html"
    return requests.get(swagger).status_code == 200


def check_azure_health(url: str) -> bool:
    # bypass 403 on azure
    headers = {
        'authority': 'www.amazon.com',
        'rtt': '50',
        'downlink': '10',
        'ect': '4g',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
    }
    response = requests.get(url, headers=headers)

    if response != 200:
        return False

    data = response.json()
    return data['status'] == 'Healthy'


def check_api_health(api: Api) -> Action:
    # get the function to check the health
    def get_func() -> Callable[[str], bool]:
        if api.check_method == 0:
            return check_swagger
        return check_azure_health

    if get_func()(api.url):
        return on_api_up(api)
    return on_api_down(api, "lets leave this for pierre to implement")
