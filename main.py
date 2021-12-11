import asyncio
import json

import rx
from rx import from_iterable, interval
from rx.operators import *
from rx.scheduler import ThreadPoolScheduler

from actions import ApiActionTypes
from api_health import check_api_health
from helpers import get_apis_from_json, do_action_when
from models import Api


async def main():
    with open('config.json') as json_config:
        json_data = json.loads(json_config.read())

    apis = get_apis_from_json(json_data)

    await from_iterable(apis).pipe(
        flat_map(lambda api: rx.merge(interval(json_data['refresh'],ThreadPoolScheduler()).pipe(map(lambda _: api)), rx.of(api))),
        flat_map(lambda api: rx.from_callable(lambda: check_api_health(api), ThreadPoolScheduler())),
        do_action_when(ApiActionTypes.api_up, lambda action: log_success(action.payload.api)),
        do_action_when(ApiActionTypes.api_down, lambda action: log_failure(action.payload.api))
    )


def log_success(api: Api):
    print(f'API {api.url} is up, env {api.env}')


def log_failure(api: Api):
    print(f'API {api.url} is down, env {api.env}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    t = loop.create_task(main())
    loop.run_until_complete(t)
