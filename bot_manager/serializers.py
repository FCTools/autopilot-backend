# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from rest_framework import serializers

from bot_manager.models import Bot


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ['name', 'type', 'campaigns_list', 'condition', 'action', 'checking_interval', 'list_type',
                  'landing_exceptions', 'status', ]
