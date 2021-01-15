# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import logging

from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

from bot_manager.models import Bot, Campaign
from bot_manager.services.helpers.scheduler import Scheduler
from bot_manager.services.helpers.condition_parser import ConditionParser


_logger = logging.getLogger(__name__)


class BotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BotForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bot
        fields = [
            "name",
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
        ]
        current_user = None

    def clean(self):
        _logger.info("Get form")
        super(BotForm, self).clean()

        _logger.info("Call super-clean")

        if not ConditionParser.bracket_sequence_is_valid(self.cleaned_data["condition"]):
            raise ValidationError("Incorrect condition.")
        _logger.info(f"Check condition for bot: {self.cleaned_data['name']}")

        schedule = self.cleaned_data["schedule"]
        _ = Scheduler().parse_schedule(schedule)  # just for valid checking

        _logger.info(f"Check schedule for bot: {self.cleaned_data['name']}")


@admin.register(Bot)
class AdminBot(admin.ModelAdmin):
    actions = None
    list_display = ['id', 'name', 'type', 'user', 'condition', 'status', 'action', 'period']
    filter_horizontal = ['campaigns_list']
    form = BotForm

    def get_queryset(self, request):
        qs = super(AdminBot, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_form(self, request, *args, **kwargs):
        form = super(AdminBot, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        return form


@admin.register(Campaign)
class AdminCampaign(admin.ModelAdmin):
    list_display = ['id', 'name']

