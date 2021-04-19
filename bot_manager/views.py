# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import json
import logging
import os
import subprocess
from copy import deepcopy

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from pydantic import ValidationError
from rest_framework import authentication, status
from rest_framework.response import Response
from rest_framework.views import APIView

from bot_manager.domains.accounts.bot import Bot
from bot_manager.domains.accounts.traffic_source import TrafficSource
from bot_manager.domains.api_models import bot
from bot_manager.forms import LogFilterForm


_logger = logging.getLogger(__name__)


def get_server_load_info():
    # total bots, enabled bots, total users, number of bytes of each type
    # cpu usage, database size

    total_bots = len(Bot.objects.all())
    enabled_bots = len(Bot.objects.filter(status=settings.ENABLED))
    zoomer_bots = len(Bot.objects.filter(type__exact=settings.PLAY_STOP_CAMPAIGN))
    optimizer_bots = len(Bot.objects.filter(type__exact=settings.INCLUDE_EXCLUDE_ZONE))

    stat = subprocess.Popen('mpstat -A', shell=True, stdout=subprocess.PIPE)
    stat_return = str(stat.stdout.read()).replace('\\t', ' ').split('\\n')
    server_info = stat_return[0]
    del stat_return[0]

    empty_lines = 0
    load_table = []

    for line in stat_return:
        if not line:
            if empty_lines == 1:
                break

            empty_lines += 1
            continue

        data = line.replace('AM', '').replace('PM', '').split()
        load_table.append(deepcopy(data))

    bots_stat = [f'Total bots: {total_bots}',
                 f'Enabled bots: {enabled_bots}',
                 f'Campaign play/stop bots: {zoomer_bots}',
                 f'Include/exclude zone bots: {optimizer_bots}',
                 f'Server load:',
                 server_info]

    return bots_stat, load_table


@login_required(login_url='/admin/login/')
def log_view(request):
    template = 'statistics_page.html'

    if request.method == "POST":
        form = LogFilterForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['log_type'] == 'server-load':
                bots_stat, load_table = get_server_load_info()

                return render(request, template,
                              context={'bots_stat': bots_stat, 'load_table': load_table, 'form': form,
                                       'log_type': 'server-load-info'})

            if form.cleaned_data['log_type'] == 'environment-log':
                env_log_path = os.getenv('ENV_LOG_PATH')
                if not env_log_path:
                    return render(request, template)

                with open(env_log_path, 'r', encoding='utf-8') as file:
                    log = file.read().split('\n')

                return render(request, template, context={'log': list(reversed(log)), 'form': form,
                                                          'log_type': 'environment log'})

            bot_id = form.cleaned_data["bot_id"]

            autopilot_engine_log_path = os.getenv("ACTIONS_LOG_PATH")
            if not autopilot_engine_log_path:
                return render(request, template)

            pattern = f'Bot id: {bot_id}'

            with open(autopilot_engine_log_path, 'r', encoding='utf-8') as file:
                log = file.read().split('\n')

            if not bot_id:
                return render(request, template, context={'bot_id': bot_id, 'log': list(reversed(log)),
                                                          'form': form, 'log_type': 'actions log'})

            result = [line for line in log if pattern in line]

            return render(request, template, context={'bot_id': bot_id, 'log': list(reversed(result)),
                                                      'form': form, 'log_type': 'actions log'})
        else:
            return render(request, template, {'form': form})

    else:
        form = LogFilterForm()
        return render(request, template, {"form": form})


class BotCreationView(APIView):
    queryset = Bot.objects.all()
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        try:
            new_bot = bot.Bot.parse_obj(request.data)
            _logger.info(str(request.data))
        except ValidationError as error:
            return Response(data={'success': False,
                                  'detail': str(error)}, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

        ts = TrafficSource.objects.get(name=new_bot.traffic_source)

        client_id = "-"
        list_id = "-"

        if new_bot.client_id:
            client_id = new_bot.client_id
        if new_bot.list_id:
            list_id = new_bot.list_id

        ignored_sources_ = ''

        if new_bot.ignored_sources:
            ignored_sources_ = '\n'.join(new_bot.ignored_sources)

        _bot = Bot.objects.create(name=new_bot.name,
                                  type=new_bot.type,
                                  user_id=new_bot.user_id,
                                  traffic_source=ts,
                                  condition=new_bot.condition,
                                  status=settings.DISABLED,
                                  action=new_bot.action,
                                  tracker=new_bot.tracker,
                                  tracker_requests_url=new_bot.tracker_requests_url,
                                  tracker_api_key=new_bot.tracker_api_key,
                                  ts_api_key=new_bot.ts_api_key,
                                  schedule=new_bot.schedule,
                                  period=new_bot.period,
                                  client_id=client_id,
                                  list_id=list_id,
                                  ignored_sources=ignored_sources_,
                                  campaigns_ids=[camp.dict() for camp in new_bot.campaigns_ids], )

        return Response(data={'success': True, 'bot_id': _bot.pk}, content_type='application/json',
                        status=status.HTTP_200_OK)


class BotUpdatingView(APIView):
    queryset = Bot.objects.all()
    authentication_classes = [authentication.TokenAuthentication]

    def put(self, request):
        try:
            if 'bot_id' not in request.data:
                return Response(data={'success': False,
                                      'error_message': 'bot_id is required'},
                                content_type='application/json', status=status.HTTP_400_BAD_REQUEST)

            bot_to_update = bot.Bot.parse_obj(request.data)
        except ValidationError as error:
            return Response(data={'success': False,
                                  'detail': str(error)}, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

        client_id = "-"
        list_id = "-"

        if bot_to_update.client_id:
            client_id = bot_to_update.client_id
        if bot_to_update.list_id:
            list_id = bot_to_update.list_id

        ignored_sources_ = ''

        if bot_to_update.ignored_sources:
            ignored_sources_ = '\n'.join(bot_to_update.ignored_sources)

        ts = TrafficSource.objects.get(name=bot_to_update.traffic_source)

        bot_to_update_db = Bot.objects.get(pk=bot_to_update.bot_id)

        bot_to_update_db.name = bot_to_update.name
        bot_to_update_db.type = bot_to_update.type
        bot_to_update_db.user_id = bot_to_update.user_id
        bot_to_update_db.traffic_source = ts
        bot_to_update_db.condition = bot_to_update.condition
        bot_to_update_db.status = settings.DISABLED
        bot_to_update_db.action = bot_to_update.action
        bot_to_update_db.ts_api_key = bot_to_update.ts_api_key
        bot_to_update_db.tracker = bot_to_update.tracker
        bot_to_update_db.tracker_requests_url = bot_to_update.tracker_requests_url
        bot_to_update_db.tracker_api_key = bot_to_update.tracker_api_key
        bot_to_update_db.schedule = bot_to_update.schedule
        bot_to_update_db.period = bot_to_update.period
        bot_to_update_db.client_id = client_id
        bot_to_update_db.list_id = list_id
        bot_to_update_db.ignored_sources = ignored_sources_
        bot_to_update_db.campaigns_ids = [json.loads(camp.json()) for camp in bot_to_update.campaigns_ids]

        bot_to_update_db.save()

        return Response(data={'success': True}, content_type='application/json', status=status.HTTP_200_OK)


class BotStartingView(APIView):
    queryset = Bot.objects.all()
    authentication_classes = [authentication.TokenAuthentication]

    def patch(self, request):
        try:
            bot_to_start_model = bot.ChangeStatusRequestBody.parse_obj(request.data)
        except ValidationError as error:
            return Response(data={'success': False,
                                  'detail': str(error)}, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

        bot_id = bot_to_start_model.bot_id
        bot_db = Bot.objects.get(pk=bot_id)

        if bot_db.status != settings.ENABLED:
            bot_db.status = settings.ENABLED
            bot_db.save()

        return Response(data={'success': True}, content_type='application/json')


class BotStoppingView(APIView):
    queryset = Bot.objects.all()
    authentication_classes = [authentication.TokenAuthentication]

    def patch(self, request):
        try:
            bot_to_stop_model = bot.ChangeStatusRequestBody.parse_obj(request.data)
        except ValidationError as error:
            return Response(data={'success': False,
                                  'detail': str(error)}, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

        bot_id = bot_to_stop_model.bot_id
        bot_db = Bot.objects.get(pk=bot_id)

        if bot_db.status != settings.DISABLED:
            bot_db.status = settings.DISABLED
            bot_db.save()

        return Response(data={'success': True}, content_type='application/json', status=status.HTTP_200_OK)


class BotDeletingView(APIView):
    queryset = Bot.objects.all()
    authentication_classes = [authentication.TokenAuthentication]

    def patch(self, request):
        try:
            bot_to_delete_model = bot.ChangeStatusRequestBody.parse_obj(request.data)
        except ValidationError as error:
            return Response(data={'success': False,
                                  'detail': str(error)}, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

        bot_db = Bot.objects.get(pk=bot_to_delete_model.bot_id)
        bot_db.delete()

        return Response(data={'success': True}, content_type='application/json', status=status.HTTP_200_OK)


class BotInfoView(APIView):
    queryset = Bot.objects.all()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        try:
            bot_model = bot.ChangeStatusRequestBody.parse_obj(request.data)
        except ValidationError as error:
            return Response(data={'success': False,
                                  'detail': str(error)}, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

        # TODO: add bot and user validating
        # TODO: need to generalize tracker mechanisms
        bot_db = Bot.objects.get(pk=bot_model.bot_id)

        bot_json = {'name': bot_db.name, 'bot_id': bot_db.pk, 'type': bot_db.type, 'status': bot_db.status,
                    'condition': bot_db.condition, 'schedule': bot_db.schedule, 'traffic_source': bot_db.traffic_source,
                    'ts_api_key': bot_db.ts_api_key, 'tracker': bot_db.tracker,
                    'tracker_requests_url': bot_db.tracker_requests_url,
                    'tracker_api_key': bot_db.tracker_api_key,
                    'campaigns_ids': bot_db.campaigns_ids, 'user_id': bot_db.user_id, 'period': bot_db.period,
                    'action': bot_db.action,
                    'ignored_sources': bot_db.ignored_sources.split('\n')}

        return Response(data={'success': True, 'info': bot_json}, content_type='application/json',
                        status=status.HTTP_200_OK)


class BotListView(APIView):
    queryset = Bot.objects.all()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        if 'user_id' not in request.data:
            return Response(data={'success': False,
                                  'detail': 'user_id required'}, content_type='application/json',
                            status=status.HTTP_400_BAD_REQUEST)

        user_id = request.data.get('user_id')
        bots_list = Bot.objects.all().filter(user_id__exact=user_id)

        bots_list_json = []

        for bot_ in bots_list:
            bots_list_json.append({'name': bot_.name, 'bot_id': bot_.pk, 'type': bot_.type,
                                   'status': bot_.status, 'condition': bot_.condition, 'schedule': bot_.schedule,
                                   'traffic_source': bot_.traffic_source, 'ts_api_key': bot_.ts_api_key,
                                   'tracker': bot_.tracker, 'tracker_api_key': bot_.tracker_api_key,
                                   'tracker_requests_url': bot_.tracker_requests_url,
                                   'campaigns_ids': bot_.campaigns_ids, 'user_id': bot_.user_id, 'period': bot_.period,
                                   'action': bot_.action, 'ignored_sources': bot_.ignored_sources.split('\n')})

        return Response(data={'success': True, 'info': bots_list_json}, content_type='application/json',
                        status=status.HTTP_200_OK)
