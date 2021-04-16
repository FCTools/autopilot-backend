# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from rest_framework import serializers

from bot_manager.models import Bot


class BotSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128, allow_null=False, allow_blank=False)

    type = serializers.IntegerField(allow_null=False)

    user_id = serializers.IntegerField(allow_null=False)

    traffic_source = serializers.IntegerField(allow_null=False)

    tracker = serializers.CharField(max_length=128, allow_null=False, allow_blank=False)

    tracker_api_key = serializers.CharField(max_length=128, allow_blank=False, allow_null=False)

    tracker_requests_url = serializers.CharField(max_length=256, allow_blank=False, allow_null=False)

    campaigns_ids = serializers.JSONField(allow_null=False)

    condition = serializers.CharField(max_length=16384, allow_null=False, allow_blank=False)

    status = serializers.CharField(max_length=8, allow_blank=False, allow_null=False)

    action = serializers.IntegerField(allow_null=False)

    ts_api_key = serializers.CharField(max_length=128, allow_null=False, allow_blank=False)

    schedule = serializers.CharField(max_length=16384, allow_blank=False, allow_null=False)

    period = serializers.IntegerField(allow_null=False)

    list_id = serializers.CharField(max_length=128, allow_null=False, allow_blank=False)

    ignored_sources = serializers.CharField(max_length=8192, allow_blank=False, allow_null=False)

    client_id = serializers.CharField(max_length=128, allow_blank=False, allow_null=False)

