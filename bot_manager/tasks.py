import json
from datetime import datetime, timedelta

import redis
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404

from bot_manager.models import Bot
from bot_manager.services.helpers.condition_parser import ConditionParser
from web.backend.celery import app


WEEKDAYS = ('mn', 'tu', 'wd', 'th', 'fr', 'sa', 'sn')


def collect_tasks():
    today = WEEKDAYS[datetime.utcnow().weekday()]
    now = datetime.utcnow()

    today_dt = datetime(now.year, now.month, now.day)

    bots_list = list(Bot.objects.filter(status__exact='enabled'))
    bot_ids = []

    for bot in bots_list:
        today_schedule = json.loads(bot.schedule)[today]

        for entry in today_schedule:
            hour, minute = entry[0], entry[1]
            today_dt.hour = hour
            today_dt.minute = minute

            if (today_dt > now and today_dt - now < timedelta(minutes=3)) or \
               (now >= today_dt and now - today_dt < timedelta(minutes=3)):
                bot_ids.append(bot.id)
                break

    return bots_list


@app.task
def check_bots():
    redis_server = redis.Redis(host=settings.REDIS_REMOTE_HOST, port=settings.REDIS_REMOTE_PORT,
                               password=settings.REDIS_REMOTE_PASSWORD)

    bots = collect_tasks()

    for bot_id in bots:
        try:
            bot = get_object_or_404(Bot, pk=bot_id)
        except Http404:
            # log it here
            continue

        if bot.type == 1:
            sites_to_act = []

            for campaign in bot.campaigns_list.all():
                sites_to_act += ConditionParser.check_sites(bot.condition, campaign.id)

            # send to redis, filter duplicates and add to internal black/white list here

        elif bot.type == 2:
            campaigns_to_act = []

            if bot.action == 4:
                status = 'play'
            elif bot.action == 3:
                status = 'paused'
            else:
                continue

            for campaign in bot.campaigns_list.all():
                if campaign.status != status and ConditionParser.check_campaign(bot.condition, campaign.id):
                    campaigns_to_act.append(campaign.id)

                    campaign.status = status
                    campaign.save()

            # send to redis, filter duplicates and set started/stopped status
