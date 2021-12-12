import asyncio
import json

import rx
from rx import from_iterable, interval, subject
from rx.operators import *
from rx.scheduler import ThreadPoolScheduler

from actions import ApiActionTypes, on_new_api_status, on_api_status_change
from api_health import check_api_health
from helpers import get_apis_from_json
from models import Api, Action, ApiStatusEnum


async def main():
    with open('config.json') as json_config:
        json_config = json.loads(json_config.read())

    apis = get_apis_from_json(json_config)

    state = {}

    api_change_obs = subject.Subject()

    # updates the state with new status
    def update_state(action: Action):
        status = ApiStatusEnum.up if action.action_type == ApiActionTypes.api_up else ApiStatusEnum.down

        if action.payload.api.url not in state:
            state[action.payload.api.url] = status
            api_change_obs.on_next(on_new_api_status(action.payload.api, status))

        state[action.payload.api.url] = status
        api_change_obs.on_next(on_api_status_change(action.payload.api, status))

    on_state_change = api_change_obs.pipe(
        filter(lambda a: a is not None),
    )

    await from_iterable(apis).pipe(
        flat_map(lambda api: rx.merge(interval(json_config['refresh'], ThreadPoolScheduler()).pipe(map(lambda _: api)),
                                      rx.of(api))),
        flat_map(lambda api: rx.from_callable(lambda: check_api_health(api), ThreadPoolScheduler())),
        do_action(update_state),
        merge(on_state_change),

    )


def log_success(api: Api):
    print(f'API {api.url} is up, env {api.env}')


def log_failure(api: Api):
    print(f'API {api.url} is down, env {api.env}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    t = loop.create_task(main())
    loop.run_until_complete(t)
