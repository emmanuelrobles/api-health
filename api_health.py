import requests as requests


def check_swagger(url: str) -> bool:
    swagger = url + "/swagger/index.html"
    return requests.get(swagger).status_code == 200


def check_azure_health(url: str) -> bool:
    data = requests.get(url).json()
    return data['status'] == 'Healthy'
