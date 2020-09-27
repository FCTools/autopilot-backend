"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from rest_framework import serializers
from .models import Bot


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ['name', 'type', 'campaigns_list', 'condition', 'action', 'checking_interval', 'list_type',
                  'landing_exceptions', ]
