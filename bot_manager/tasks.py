"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

import json
from datetime import datetime, timedelta

import redis
from django.conf import settings

from bot_manager.models import Bot
from bot_manager.services.helpers.condition_parser import ConditionParser
from bot_manager.services.tracker.updater import Updater
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
        print(today_schedule)
        print(today)

        for entry in today_schedule:
            hour, minute = entry[0], entry[1]
            tmp = datetime(year=today_dt.year, month=today_dt.month, day=today_dt.day, hour=hour, minute=minute)

            if (tmp > now and tmp - now <= timedelta(minutes=3)) or \
                    (now >= tmp and now - tmp <= timedelta(minutes=3)):
                bot_ids.append(bot)
                break

    return bot_ids


@app.task
def update():
    Updater.update()


@app.task
def check_bots():
    redis_server = redis.Redis(host=settings.REDIS_REMOTE_HOST, port=settings.REDIS_REMOTE_PORT,
                               password=settings.REDIS_REMOTE_PASSWORD)

    bots = collect_tasks()
    print(bots)

    for bot in bots:
        if bot.type == 1:
            sites_to_act = []

            for campaign in bot.campaigns_list.all():
                sites_to_act += ConditionParser.check_sites(bot.condition, campaign.id)

            if redis_server.exists(str(bot.pk)):
                prev_info = json.loads(redis_server.get(str(bot.pk)))
                redis_server.delete(str(bot.pk))
                prev_info += sites_to_act
                redis_server.append(str(bot.pk), json.dumps(list(set(prev_info))))
            else:
                redis_server.append(str(bot.pk), json.dumps(list(set(sites_to_act))))

        elif bot.type == 2:
            campaigns_to_act = []

            if bot.action == 4:
                status = 'play'
            elif bot.action == 3:
                status = 'paused'
            else:
                continue

            for campaign in bot.campaigns_list.all():
                if campaign.status != status and ConditionParser.check_campaign(bot.condition, campaign.id, bot.period):
                    campaigns_to_act.append(campaign.id)

                    campaign.status = status
                    campaign.save()

            # send to redis, filter duplicates and set started/stopped status
