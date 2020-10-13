"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

import json
from copy import copy
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
    redis_server = redis.Redis(host=settings.REDIS_REMOTE_HOST, port=settings.REDIS_REMOTE_PORT,
                               password=settings.REDIS_REMOTE_PASSWORD)

    bots = collect_tasks()
    print(bots)

    for bot in bots:
        if bot.type == 1:
            sites_to_act = []
            ignored_sources = json.loads(bot.ignored_sources)

            for campaign in bot.campaigns_list.all():
                sites_to_act_tmp = ConditionParser.check_sites(bot.condition, campaign.id, bot.period, bot.action)
                for site in sites_to_act_tmp:
                    if site not in ignored_sources:
                        sites_to_act.append(copy(site))

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
            current_source_info = json.loads(bot.source_info)

            for campaign in bot.campaigns_list.all():
                campaigns_to_act_tmp = ConditionParser.check_campaign(bot.condition, campaign.id, bot.period)

                for campaign_tmp in campaigns_to_act_tmp:
                    camp_to_add = {'tracker_id': copy(campaign.id), 'source_id': copy(campaign_tmp)}
                    camp_index = current_source_info.index(camp_to_add)

                    if current_source_info[camp_index]['status'] == 'started' and bot.action == 4 or \
                            current_source_info[camp_index]['status'] == 'stopped' and bot.action == 3:
                        continue

                    campaigns_to_act.append(camp_to_add)

                    if bot.action == 3:
                        current_source_info[camp_index]['status'] = 'stopped'
                    else:
                        current_source_info[camp_index]['status'] = 'started'

            bot.source_info = json.dumps(current_source_info)
            bot.save()

            if redis_server.exists(str(bot.pk)):
                prev_info = json.loads(redis_server.get(str(bot.pk)))
                redis_server.delete(str(bot.pk))
                prev_info['campaigns_ids'] += campaigns_to_act
                redis_server.append(str(bot.pk), json.dumps({'campaigns_ids': prev_info['campaigns_ids'],
                                                             'action': bot.action}))
            else:
                if campaigns_to_act:
                    redis_server.append(str(bot.pk), json.dumps({'campaigns_ids': campaigns_to_act,
                                                                 'action': bot.action}))
