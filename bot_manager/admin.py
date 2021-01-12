# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from django.contrib import admin
from django import forms

from bot_manager.models import Bot, Campaign
from bot_manager.services.helpers.scheduler import Scheduler


class BotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BotForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bot
        fields = [
            "type",
            "user",
            "traffic_source",
            "campaigns_list",
            "condition",
            "status",
            "action",
            "ts_api_key",
            "schedule",
            "period",
            "ignored_sources",
        ]

    def clean(self):
        scheduler = Scheduler()
        super(BotForm, self).clean()
        schedule = self.cleaned_data["schedule"]

        scheduler.parse_schedule(schedule)


@admin.register(Bot)
class AdminBot(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'user', 'condition', 'status', 'action', 'period']
    form = BotForm


@admin.register(Campaign)
class AdminCampaign(admin.ModelAdmin):
    list_display = ['id', 'name']

