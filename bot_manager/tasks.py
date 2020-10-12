"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

import json
from datetime import datetime, timedelta

import redis
from django.conf import settings

from bot_manager.models import Bot, TrafficSource
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
        # print(today_schedule)
        # print(today)

        for entry in today_schedule:
            hour, minute = entry[0], entry[1]
            tmp = datetime(year=today_dt.year, month=today_dt.month, day=today_dt.day, hour=hour, minute=minute)

            if (tmp > now and tmp - now <= timedelta(minutes=2)) or \
                    (now >= tmp and now - tmp <= timedelta(minutes=2)):
                bot_ids.append(bot)
                break

    return bot_ids


@app.task
def update():
    Updater.update()


@app.task
def check_bots():
    traffic_sources_list = list(TrafficSource.objects.all())

    for traffic_source in traffic_sources_list:
        if 'PushAds' in traffic_source.name:
            traffic_source.filtering_param_number_sources = 27
            traffic_source.filtering_param_name_sources = 'sid'
            traffic_source.filtering_param_name_campaigns = 'cid'
            traffic_source.filtering_param_number_campaigns = 283

            traffic_source.save()

    redis_server = redis.Redis(host=settings.REDIS_REMOTE_HOST, port=settings.REDIS_REMOTE_PORT,
                               password=settings.REDIS_REMOTE_PASSWORD)

    bots = collect_tasks()
    print(bots)

    for bot in bots:
        if bot.type == 1:
            sites_to_act = []

            for campaign in bot.campaigns_list.all():
                sites_to_act += ConditionParser.check_sites(bot.condition, campaign.id, bot.period, bot.action)

            if redis_server.exists(str(bot.pk)):
                prev_info = json.loads(redis_server.get(str(bot.pk)))
                redis_server.delete(str(bot.pk))
                prev_info['sources_list'] += sites_to_act
                redis_server.append(str(bot.pk), json.dumps({'sources_list': list(set(prev_info['sources_list'])),
                                                             'action': bot.action}))
            else:
                if sites_to_act:
                    redis_server.append(str(bot.pk), json.dumps({'sources_list': list(set(sites_to_act)),
                                                                 'action': bot.action}))

        elif bot.type == 2:
            campaigns_to_act = []

            for campaign in bot.campaigns_list.all():
                if campaign.status != bot.action and ConditionParser.check_campaign(bot.condition, campaign.id, bot.period,
                                                                                bot.action):
                    campaigns_to_act.append(campaign.id)

                    campaign.status = bot.action
                    campaign.save()

            if redis_server.exists(str(bot.pk)):
                prev_info = json.loads(redis_server.get(str(bot.pk)))
                redis_server.delete(str(bot.pk))
                prev_info['campaigns_list'] += campaigns_to_act
                redis_server.append(str(bot.pk), json.dumps({'campaigns_list': list(set(prev_info['campaigns_list'])),
                                                             'action': bot.action}))
            else:
                if campaigns_to_act:
                    redis_server.append(str(bot.pk), json.dumps({'campaigns_list': list(set(campaigns_to_act)),
                                                                 'action': bot.action}))
