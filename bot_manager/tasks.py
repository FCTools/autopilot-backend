from datetime import datetime, timedelta

import redis
from django.conf import settings

from bot_manager.models import Bot
from bot_manager.services.helpers.condition_parser import ConditionParser
from web.backend.celery import app


@app.task
def check_bots():
    redis_server = redis.Redis(host=settings.REDIS_REMOTE_HOST, port=settings.REDIS_REMOTE_PORT,
                               password=settings.REDIS_REMOTE_PASSWORD)

    bots = Bot.objects.filter(status="enabled")

    for bot in bots:
        if bot.last_checked and bot.last_checked - datetime.utcnow() > timedelta(seconds=bot.checking_interval):
            continue

        if bot.type == 1:
            sites_to_act = []

            for campaign in bot.campaigns_list.all():
                sites_to_act += ConditionParser.check_sites(bot.condition, campaign.id)

            # send to redis, filter duplicates and add to internal black/white list here

        elif bot.type == 2:
            campaigns_to_act = []

            if bot.action == 'start_camp':
                status = 'play'
            else:
                status = 'pause'

            for campaign in bot.campaigns_list.all():
                if ConditionParser.check_campaign(bot.condition, campaign.id):
                    campaigns_to_act.append(campaign.id)

                    campaign.status = status
                    campaign.save()

            # send to redis, filter duplicates and set started/stopped status

        bot.last_checked = datetime.utcnow()
