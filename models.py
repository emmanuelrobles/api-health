from enum import Enum
from typing import Generic, TypeVar, List

T = TypeVar("T")


class Api:
    def __init__(self, url: str, check_method: int):
        self.url = url
        self.check_method = check_method


class Action(Generic[T]):
    def __init__(self, action_type: str, payload: T):
        self.action_type = action_type
        self.payload = payload


class CheckApiAction:
    def __init__(self, api: Api):
        self.api = api


class ApiUpAction:
    def __init__(self, api: Api):
        self.api = api


class ApiDownAction:
    def __init__(self, api: Api, msg: str = ''):
        self.api = api
        self.msg = msg


class NewApiStatusAction:
    def __init__(self, api: Api, status: str = ''):
        self.api = api
        self.status = status


class ApiStatusChangeAction:
    def __init__(self, api: Api, status: str = ''):
        self.api = api
        self.status = status


class ApiStatusEnum(str, Enum):
    up = "Up",
    down = "Down"
