from typing import Generic, TypeVar

T = TypeVar("T")


class Api:
    def __init__(self, url: str, check_method: int, env: str):
        self.url = url
        self.check_method = url
        self.env = url


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
    def __init__(self, api: Api, error: str):
        self.api = api
        self.error = error
