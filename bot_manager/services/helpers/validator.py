from bot_manager.models import Campaign, User, Bot
from bot_manager.services.tracker.updater import Updater

AVAILABLE_ACTIONS = ("stop_campaign", "start_campaign", "add_to_bl", "add_to_wl")


class Validator:
    @staticmethod
    def validate_new_bot_data(data):
        if 'name' in data:
            name = data.get('name')

            if len(name) == 0:
                return "name field can't be empty"
            elif len(name) > 128:
                return "too long name (max: 120 symbols)"
        else:
            return 'name field is required'

        if 'type' in data:
            try:
                bot_type = int(data.get('type'))
            except ValueError:
                return 'invalid bot type - not a number'

            if bot_type != 1 and bot_type != 2:
                return 'bot type can be only 1 or 2'
        else:
            return 'type field is required'

        if 'condition' in data:
            condition = data.get('condition')
            # check condition here
        else:
            return 'condition field is required'

        if 'action' in data:
            action = data.get('action')

            if action not in AVAILABLE_ACTIONS:
                return 'invalid action'
        else:
            return 'action field is required'

        if 'interval' in data:
            interval = data.get('interval')

            if interval < 120:
                return "checking interval can't be less than 120 seconds"
        else:
            return 'interval field is required'

        if bot_type == 1:
            if 'list_type' in data:
                list_type = data.get('list_type')

                if list_type != 'black' and list_type != 'white':
                    return 'invalid list type'
            else:
                return 'list_type is required for bots of type 1'

        if 'user_id' in data:
            user_id = data.get('user_id')
            user = list(User.objects.filter(id__exact=user_id))

            if not user:
                Updater.update()
                updated = True

            user = list(User.objects.filter(id__exact=user_id))

            if not user:
                return 'unknown user'

        else:
            return 'user_id field is required'

        if 'campaigns' in data:
            campaigns_ids = data.get('campaigns')

            for campaign_id in campaigns_ids:
                campaign_db = list(Campaign.objects.filter(id__exact=campaign_id))

                if not campaign_db:
                    if not updated:
                        Updater.update()
                        updated = True
                    else:
                        return f'unknown campaign: {campaign_id}'

                campaign_db = list(Campaign.objects.filter(id__exact=campaign_id))

                if not campaign_db:
                    return f'unknown campaign: {campaign_id}'

                campaign = campaign_db[0]
                if campaign.user_id != user_id:
                    return f'campaign {campaign_id} pinned to another user'

        else:
            return 'campaigns field is required'

        user_bots = Bot.objects.filter(user_id=user_id)

        for bot in user_bots:
            if bot.name == name:
                return 'this user already has bot with this name'

        return "valid"
