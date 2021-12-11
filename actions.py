from enum import Enum

from models import Api, Action, ApiUpAction, CheckApiAction, ApiDownAction


def on_check_api(api: Api) -> Action[CheckApiAction]:
    return Action(ApiActionTypes.api_up, CheckApiAction(api))


def on_api_up(api: Api) -> Action[ApiUpAction]:
    return Action(ApiActionTypes.api_up, ApiUpAction(api))


def on_api_down(api: Api, error: str) -> Action[ApiDownAction]:
    return Action(ApiActionTypes.api_up, ApiDownAction(api,error))


class ApiActionTypes(str, Enum):
    check_api = 'check_api'
    api_up = 'api_up'
    api_down = 'api_down'
