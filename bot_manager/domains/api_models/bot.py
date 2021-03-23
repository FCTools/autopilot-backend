# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from typing import List

from django.conf import settings
from pydantic import BaseModel, validator


class Campaign(BaseModel):
    source_id: str
    tracker_id: int


class Bot(BaseModel):
    name: str
    type: int
    user_id: int
    condition: str
    schedule: List[str]
    traffic_source: str
    ts_api_key: str
    tracker: str
    tracker_api_key: str
    campaigns_ids: List[Campaign]
    period: int
    action: int
    ignored_sources: List[str]

    @validator('type', allow_reuse=True)
    def type_is_valid(cls, type_):
        assert (type_ == 1 or type_ == 2)
        return type_

    @validator('user_id', allow_reuse=True)
    def valid_user_id(cls, user_id):
        assert user_id > 0
        return user_id

    @validator('condition', allow_reuse=True)
    def condition_is_valid(cls, condition):
        # TODO: add condition validation
        return condition

    @validator('schedule', allow_reuse=True)
    def schedule_id_valid(cls, schedule):
        # TODO: add schedule validation
        return schedule

    @validator('traffic_source', allow_reuse=True)
    def ts_is_valid(cls, ts):
        # TODO: add supported traffic sources
        assert ts in []
        return ts

    @validator('period', allow_reuse=True)
    def period_is_valid(cls, period):
        assert period in [1, 2, 3, 4, 5, 6, 7, 9, 11, 13, 14]
        return period

    @validator('action', allow_reuse=True)
    def action_is_valid(cls, action):
        assert action in [settings.PLAY_CAMPAIGN,
                          settings.STOP_CAMPAIGN,
                          settings.EXCLUDE_ZONE,
                          settings.INCLUDE_ZONE]
        return action

    @validator('ignored_sources', allow_reuse=True)
    def ignored_sources_is_valid(cls, ignored_sources):
        # TODO: implement validation
        return ignored_sources

    @validator('ts_api_key', allow_reuse=True)
    def ts_api_key_is_valid(cls, ts_api_key):
        # TODO: implement validation
        return ts_api_key

    @validator('tracker', allow_reuse=True)
    def tracker_is_valid(cls, tracker):
        # TODO: implement validation
        return tracker

    @validator('tracker_api_key', allow_reuse=True)
    def tracker_api_key_is_valid(cls, tracker_api_key):
        # TODO: implement validation
        return tracker_api_key

# class CreateRequestBody(BaseModel):
#     pass
#
#
# class UpdateRequestBody(BaseModel):
#     pass
#
#
# class DeleteRequestBody(BaseModel):
#     pass
#
#
# class StartRequestBody(BaseModel):
#     pass
#
#
# class StopRequestBody(BaseModel):
#     pass
#
#
# class ListRequestBody(BaseModel):
#     pass
#
#
# class BotInfoRequestBody(BaseModel):
#     pass
