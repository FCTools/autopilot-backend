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
    campaigns_ids: List[Campaign]
    period: int
    action: int
    ignored_sources: List[str]

    @validator('type')
    def valid_type(self, type_):
        assert (type_ == 1 or type_ == 2)
        return type_

    @validator('user_id')
    def valid_user_id(self, user_id):
        assert user_id > 0
        return user_id

    @validator('condition')
    def condition_is_valid(self, condition):
        # TODO: add condition validation
        return condition

    @validator('schedule')
    def schedule_id_valid(self, schedule):
        # TODO: add schedule validation
        return schedule

    @validator('traffic_source')
    def ts_is_valid(self, ts):
        # TODO: add supported traffic sources
        assert ts in []
        return ts

    @validator('period')
    def period_is_valid(self, period):
        assert period in [1, 2, 3, 4, 5, 6, 7, 9, 11, 13, 14]
        return period

    @validator('action')
    def action_is_valid(self, action):
        assert action in [settings.PLAY_CAMPAIGN,
                          settings.STOP_CAMPAIGN,
                          settings.EXCLUDE_ZONE,
                          settings.INCLUDE_ZONE]
        return action

    @validator('ignored_sources')
    def ignored_sources_is_valid(self, ignored_sources):
        # TODO: implement validation
        return ignored_sources


class CreateRequestBody(BaseModel):
    pass


class UpdateRequestBody(BaseModel):
    pass


class DeleteRequestBody(BaseModel):
    pass


class StartRequestBody(BaseModel):
    pass


class StopRequestBody(BaseModel):
    pass


class ListRequestBody(BaseModel):
    pass


class BotInfoRequestBody(BaseModel):
    pass
