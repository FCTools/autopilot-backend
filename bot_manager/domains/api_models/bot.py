# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from typing import List, Optional, Union, Dict

from django.conf import settings
from pydantic import BaseModel, validator

from bot_manager.services.helpers import scheduler


class Campaign(BaseModel):
    source_id: str
    tracker_id: str


class Bot(BaseModel):
    name: str
    type: int
    user_id: int
    condition: str
    schedule: str
    traffic_source: str
    ts_api_key: Dict
    tracker: str
    tracker_requests_url: str
    status: str
    tracker_api_key: str
    campaigns_ids: List[Campaign]
    period: int
    action: int
    client_key: Optional[Union[str, None]]
    list_id: Optional[Union[str, None]]
    ignored_sources: Optional[Union[List[str], None]]
    bot_id: Optional[int]

    @validator('name', allow_reuse=True)
    def name_is_valid(cls, name):
        # TODO: check that name is unique
        assert name, "name can't be empty"
        assert len(name), f'name must contain at least 1 character'
        assert len(name) <= 128, f'name must contain less than 128 characters'
        return name

    @validator('type', allow_reuse=True)
    def type_is_valid(cls, type_):
        assert type_, "type can't be empty"
        assert type_ in [settings.INCLUDE_EXCLUDE_ZONE, settings.PLAY_STOP_CAMPAIGN], f'incorrect bot type: {type_}'
        return type_

    @validator('user_id', allow_reuse=True)
    def valid_user_id(cls, user_id):
        assert user_id, "user_id can't be empty"
        assert user_id > 0, f'incorrect user_id (< 0)'
        return user_id

    @validator('condition', allow_reuse=True)
    def condition_is_valid(cls, condition):
        # TODO: add condition validation
        assert condition, "condition can't be empty"
        assert len(condition) >= 6, f'condition must contain at least 6 characters'
        assert len(condition) <= 16384, f'condition must contain less than 16 384 characters'

        return condition

    @validator('schedule', allow_reuse=True)
    def schedule_id_valid(cls, schedule):
        assert schedule, "schedule can't be empty"
        try:
            _ = scheduler.Scheduler().parse_schedule(schedule)
        except (ValueError, IndexError):
            raise ValueError('incorrect schedule')

        return schedule

    @validator('traffic_source', allow_reuse=True)
    def ts_is_valid(cls, ts):
        assert ts, "ts can't be empty"
        assert ts in settings.SUPPORTED_TRAFFIC_SOURCES, f"incorrect traffic source: {ts}"
        return ts

    @validator('period', allow_reuse=True)
    def period_is_valid(cls, period):
        assert period in settings.SUPPORTED_PERIODS, f'incorrect period: {period}'
        return period

    @validator('action', allow_reuse=True)
    def action_is_valid(cls, action):
        assert action, "action can't be empty"
        assert action in settings.SUPPORTED_ACTIONS, f'incorrect action: {action}'
        return action

    @validator('ignored_sources', allow_reuse=True)
    def ignored_sources_is_valid(cls, ignored_sources):
        # TODO: implement validation
        return ignored_sources

    @validator('ts_api_key', allow_reuse=True)
    def ts_api_key_is_valid(cls, ts_api_key):
        assert ts_api_key, "ts_api_key can't be empty"
        assert len(ts_api_key) >= 1, 'ts_api_key must contain at least 1 character'
        assert len(ts_api_key) < 128, 'ts_api_key must contain less than 128 characters'
        return ts_api_key

    @validator('tracker', allow_reuse=True)
    def tracker_is_valid(cls, tracker):
        assert tracker, "tracker can't be empty"
        assert tracker in settings.SUPPORTED_TRACKERS, f'incorrect tracker: {tracker}'
        return tracker

    @validator('tracker_api_key', allow_reuse=True)
    def tracker_api_key_is_valid(cls, tracker_api_key):
        assert tracker_api_key, "tracker_api_key can't be empty"
        assert len(tracker_api_key) >= 1, 'tracker_api_key must contain at least 1 character'
        assert len(tracker_api_key) < 128, 'tracker_api_key must contain less than 128 characters'
        return tracker_api_key

    @validator('status', allow_reuse=True)
    def status_is_valid(cls, status):
        assert status, "status can't be empty"
        assert status in [settings.ENABLED, settings.DISABLED], f'incorrect status: {status}'
        return status

    @validator('client_key', allow_reuse=True)
    def client_key_is_valid(cls, client_key):
        if client_key is not None:
            assert len(client_key) >= 1, 'client_key must contain at least 1 character'
            assert len(client_key) < 128, 'client_key must contain less than 128 characters'

        return client_key

    @validator('list_id', allow_reuse=True)
    def client_key_is_valid(cls, list_id):
        if list_id is not None:
            assert len(list_id) >= 1, 'list_id must contain at least 1 character'
            assert len(list_id) < 128, 'list_id must contain less than 128 characters'

        return list_id


class ChangeStatusRequestBody(BaseModel):
    bot_id: int
    user_id: int
