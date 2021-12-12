import asyncio
import json

import rx
from rx import from_iterable, interval, subject
from rx.operators import *
from rx.scheduler import ThreadPoolScheduler

from actions import ApiActionTypes, on_new_api_status, on_api_status_change
from api_health import check_api_health
from helpers import get_apis_from_json, do_action_when, of_type
from models import Api, Action, ApiStatusEnum
from notifications import teams_build_new_api_payload, notify_request


async def main():
    with open('config.json') as json_config:
        json_config = json.loads(json_config.read())

    apis = get_apis_from_json(json_config)

    state = {}

    api_change_subject = Subject()

    new_api_subject = Subject()
    api_status_change_subject = Subject()

    # updates the state with new status
    def update_state(action: Action):
        status = ApiStatusEnum.up if action.action_type == ApiActionTypes.api_up else ApiStatusEnum.down

        if action.payload.api.url not in state:
            state[action.payload.api.url] = status
            api_change_subject.on_next(on_new_api_status(action.payload.api, status))

        # push if the status has changed
        if state[action.payload.api.url] != status:
            state[action.payload.api.url] = status
            api_change_subject.on_next(on_api_status_change(action.payload.api, status))

    # handles state changes
    on_state_change = api_change_subject.pipe(
        filter(lambda a: a is not None),
        do_action_when(ApiActionTypes.new_api_status, lambda a: new_api_subject.on_next(a)),
        do_action_when(ApiActionTypes.api_status_change, lambda a: api_status_change_subject.on_next(a))
    )

    # act on new api received
    new_api_obs = new_api_subject.pipe(
        of_type(ApiActionTypes.new_api_status),
        map(lambda a: a.payload),
        buffer_with_time(timedelta(seconds=1)),
        filter(lambda a: len(a) != 0),
        do_action(lambda d: notify_request(teams_build_new_api_payload(d), json_config['request_notification']["url"]))
    )

    # act on api state change
    api_status_change_obs = api_status_change_subject.pipe(
        of_type(ApiActionTypes.api_status_change),
        map(lambda a: a.payload),
        buffer_with_time(timedelta(seconds=1)),
        filter(lambda a: len(a) != 0),
        do_action(lambda d: notify_request(teams_build_new_api_payload(d), json_config['request_notification']["url"]))
    )

    # main obs
    await from_iterable(apis).pipe(
        flat_map(lambda api: rx.merge(interval(json_config['refresh'], ThreadPoolScheduler()).pipe(map(lambda _: api)),
                                      rx.of(api))),
        flat_map(lambda api: rx.from_callable(lambda: check_api_health(api), ThreadPoolScheduler())),
        do_action(update_state),
        merge(on_state_change, new_api_obs, api_status_change_obs)
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    t = loop.create_task(main())
    loop.run_until_complete(t)
