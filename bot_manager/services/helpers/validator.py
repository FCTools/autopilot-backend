"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.http import Http404
from django.shortcuts import get_object_or_404

from bot_manager.models import Campaign, User, Bot
from bot_manager.services.helpers.condition_parser import ConditionParser

AVAILABLE_ACTIONS = (1, 2, 3, 4, )


class Validator:
    @staticmethod
    def validate_new_bot(data, bot_exists=False, user_id=None):
        if 'name' in data:
            name = data.get('name')

            if len(name) == 0:
                return False, "name field can't be empty"
            elif len(name) > 128:
                return False, 'too long name (max: 120 symbols)'
        else:
            return False, 'name field is required'

        if 'type' in data:
            try:
                bot_type = int(data.get('type'))
            except ValueError:
                return False, 'invalid bot type - not a number'

            # type 1 - black/white lists, type 2 - start/stop campaigns
            if bot_type != 1 and bot_type != 2:
                return False, 'bot type can be only 1 or 2'
        else:
            return False, 'type field is required'

        if 'condition' in data:
            condition = data.get('condition')

            if not ConditionParser.is_valid(condition):
                return False, 'invalid condition'

        else:
            return False, 'condition field is required'

        if 'action' in data:
            action = int(data.get('action'))

            if action not in AVAILABLE_ACTIONS:
                return False, 'invalid action'
        else:
            return False, 'action field is required'

        if bot_type == 1:
            if action != 1 and action != 2:  # 2 - black list, 1 - white list
                return False, 'invalid action for bot type 1'
        elif bot_type == 2:
            if action != 3 and action != 4:  # 3 - stop camp, 4 - start camp
                return False, 'invalid action for bot type 2'

        if not bot_exists:
            if 'user_id' in data:
                user_id = int(data.get('user_id'))

                try:
                    user = get_object_or_404(User, pk=user_id)
                except Http404:
                    return False, 'unknown user'

            else:
                return False, 'user_id field is required'

        if 'campaigns_ids' in data:
            campaigns_ids = [int(camp_id) for camp_id in data.get('campaigns_ids')]

            if not campaigns_ids:
                return False, "campaigns list can't be empty"

            for campaign_id in campaigns_ids:
                try:
                    campaign_db = get_object_or_404(Campaign, pk=campaign_id)
                except Http404:
                    return False, f'unknown campaign: {campaign_id}'

                if campaign_db.user_id != user_id:
                    return False, f'campaign {campaign_id} pinned to another user'

        else:
            return False, 'campaigns_ids field is required'

        if 'ignored_sources' in data:
            ignored_sources = data.get('ignored_sources')

            # check sources here

        if 'schedule' in data:
            schedule = data.get('schedule')

            for entry in schedule:
                if '-' in entry:
                    parts = entry.split('-')
                    if parts[0] not in ['mn', 'tu', 'wd', 'th', 'fr', 'sa', 'sn']:
                        return False, f'incorrect weekday: {entry}'

                    if ':' in parts[1]:
                        time_parts = parts[1].split(':')
                    else:
                        return False, f'incorrect time: {entry}'

                    try:
                        num_1 = int(time_parts[0])
                        num_2 = int(time_parts[1])
                    except ValueError:
                        return False, f'incorrect time: {entry}'

                    if not ((0 <= num_1 <= 23) and (0 <= num_2 <= 59)):
                        return False, f'incorrect time: {entry}'
                else:
                    return False, 'incorrect schedule'

        else:
            return False, 'schedule field is required'

        if 'period' in data:
            period = data.get('period')

            try:
                period = int(period)
            except ValueError:
                return False, "can't convert period to int (not a number)"

            if period < 0:
                return False, "period can't be less than zero"
        else:
            return False, 'period field is required'

        if not bot_exists:
            user_bots = Bot.objects.filter(user_id__exact=user_id)

            for bot in user_bots:
                if bot.name == name:
                    return False, 'this user already has bot with this name'

        return True, 'ok'
