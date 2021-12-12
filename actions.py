from enum import Enum

from models import Api, Action, ApiUpAction, CheckApiAction, ApiDownAction, NewApiStatusAction, ApiStatusChangeAction


# Maybe for future usage
def on_check_api(api: Api) -> Action[CheckApiAction]:
    return Action(ApiActionTypes.api_up, CheckApiAction(api))


def on_api_up(api: Api) -> Action[ApiUpAction]:
    return Action(ApiActionTypes.api_up, ApiUpAction(api))


def on_api_down(api: Api, msg: str) -> Action[ApiDownAction]:
    return Action(ApiActionTypes.api_up, ApiDownAction(api, msg))


def on_new_api_status(api: Api, status: str) -> Action[NewApiStatusAction]:
    return Action(ApiActionTypes.new_api_status, NewApiStatusAction(api, status))


def on_api_status_change(api: Api, status: str) -> Action[ApiStatusChangeAction]:
    return Action(ApiActionTypes.api_status_change, ApiStatusChangeAction(api, status))


class ApiActionTypes(str, Enum):
    check_api = 'check_api'
    api_up = 'api_up'
    api_down = 'api_down'
    new_api_status = 'new_api_status'
    api_status_change = 'api_status_change'
