from typing import List, Callable

from rx import operators, Observable

from models import Api, Action


def get_apis_from_json(json_data: dict) -> List[Api]:
    json_apis = json_data['apis']

    apis = []
    for json_api in json_apis:
        for env in json_api['env']:
            url: str = json_api['url']

            if url.endswith('/'):
                url = url[:-1]

            apis.append(Api(url.format(env), json_api['check_method']))

    return apis


# Do action on action_type
def do_action_when(action_type: str, callback: Callable[[Action], None]) -> Callable[[Observable], Observable]:
    return operators.do_action(lambda action: callback(action) if action.action_type == action_type else None)


def of_type(action_type: str) -> Callable[[Observable], Observable]:
    return operators.filter(lambda action: action.action_type == action_type)

