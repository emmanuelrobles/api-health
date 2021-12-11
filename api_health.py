from collections import Callable

import requests as requests

from actions import on_api_up, on_api_down
from models import Api, Action


def check_swagger(url: str) -> bool:
    swagger = url + "/swagger/index.html"
    return requests.get(swagger).status_code == 200


def check_azure_health(url: str) -> bool:
    data = requests.get(url).json()
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
