# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import logging

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from bot_manager.domains.accounts.traffic_source import TrafficSource
from bot_manager.models import Bot
from bot_manager.services.helpers.condition_parser import ConditionParser
from bot_manager.services.helpers.scheduler import Scheduler

_logger = logging.getLogger(__name__)


class BotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BotForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bot
        fields = [
            "name",
            "type",
            "user_id",
            "traffic_source",
            "campaigns_list",
            "condition",
            "tracker",
            "tracker_url",
            "tracker_api_key",
            "status",
            "action",
            "ts_api_key",
            "schedule",
            "period",
            "ignored_zones",
            "list_to_add",
            "client_id",
        ]
        current_user = None

    def clean(self):
        _logger.info("Get form")
        super(BotForm, self).clean()
        _logger.info("Call super-clean")

        if not self.current_user.is_superuser and self.current_user.id != self.cleaned_data['user_id'].id:
            raise ValidationError("You can't create bot for another user.")

        self.cleaned_data['ignored_zones'] = self.cleaned_data['ignored_zones'].strip()

        if not ConditionParser.bracket_sequence_is_valid(self.cleaned_data["condition"]):
            raise ValidationError("Incorrect condition.")
        _logger.info(f"Check condition for bot: {self.cleaned_data['name']}")

        schedule = self.cleaned_data["schedule"]
        Scheduler().parse_schedule(schedule)  # just for valid checking

        _logger.info(f"Check schedule for bot: {self.cleaned_data['name']}")


@admin.register(Bot)
class AdminBot(admin.ModelAdmin):
    actions = None
    list_display = ['id', 'name', 'type', 'user_id', 'condition', 'status', 'action', 'period', ]
    form = BotForm

    def get_queryset(self, request):
        qs = super(AdminBot, self).get_queryset(request)
        if request.user_id.is_superuser:
            return qs
        return qs.filter(user=request.user_id)

    def get_form(self, request, *args, **kwargs):
        form = super(AdminBot, self).get_form(request, *args, **kwargs)
        form.current_user = request.user_id
        return form


@admin.register(TrafficSource)
class AdminTrafficSource(admin.ModelAdmin):
    list_display = ['name', 'binom_param_number']

