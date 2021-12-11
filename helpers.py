from typing import List

from models import Api


def get_apis_from_json(json_data: dict) -> List[Api]:
    json_apis = json_data['apis']

    apis = []
    for json_api in json_apis:
        apis.append(Api(json_api['url'], json_api['check_method'], json_api['env']))

    return apis
