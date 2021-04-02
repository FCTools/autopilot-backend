# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>
import json
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from pydantic import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from bot_manager.domains.accounts.bot import Bot
from bot_manager.domains.accounts.traffic_source import TrafficSource
from bot_manager.domains.api_models import bot
from bot_manager.forms import LogFilterForm


@login_required(login_url='/admin/login/')
def log_view(request):
    template = 'statistics_page.html'

    if request.method == "POST":
        form = LogFilterForm(request.POST)

        if form.is_valid():
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

    def post(self, request):
        try:
            new_bot = bot.Bot.parse_obj(request.data)
        except ValidationError as error:
            return Response(data={'success': False,
                                  'error_message': str(error)}, content_type='application/json', status=400)

        ts = TrafficSource.objects.get(name=new_bot.traffic_source)

        Bot.objects.create(name=new_bot.name,
                           type=new_bot.type,
                           user=new_bot.user_id,
                           traffic_source=ts,
                           condition=new_bot.condition,
                           status='disabled',
                           action=new_bot.action,
                           ts_api_key=new_bot.ts_api_key,
                           schedule=new_bot.schedule,
                           period=new_bot.period,
                           ignored_zones=new_bot.ignored_sources,
                           campaigns_list=[json.loads(camp.json()) for camp in new_bot.campaigns_ids], )

        return Response(data={'success': True}, content_type='application/json')


class BotUpdatingView(APIView):
    queryset = Bot.objects.all()

    def put(self, request):
        try:
            if 'bot_id' not in request.data:
                return Response(data={'success': False,
                                      'error_message': 'bot_id is required'},
                                content_type='application/json', status=400)

            bot_to_update = bot.Bot.parse_obj(request.data)
        except ValidationError as error:
            return Response(data={'success': False,
                                  'error_message': str(error)}, content_type='application/json', status=400)

        ts = TrafficSource.objects.get(name=bot_to_update.traffic_source)

        bot_to_update_db = Bot.objects.get(pk=bot_to_update.bot_id)

        bot_to_update_db.name = bot_to_update.name
        bot_to_update_db.type = bot_to_update.type
        bot_to_update_db.user = bot_to_update.user_id
        bot_to_update_db.traffic_source = ts
        bot_to_update_db.condition = bot_to_update.condition
        bot_to_update_db.status = 'disabled'
        bot_to_update_db.action = bot_to_update.action
        bot_to_update_db.ts_api_key = bot_to_update.ts_api_key
        bot_to_update_db.schedule = bot_to_update.schedule
        bot_to_update_db.period = bot_to_update.period
        bot_to_update_db.ignored_zones = bot_to_update.ignored_sources
        bot_to_update_db.campaigns_list = [json.loads(camp.json()) for camp in bot_to_update.campaigns_ids]

        bot_to_update_db.save()

        return Response(data={'success': True}, content_type='application/json')


class BotStartingView(APIView):
    def patch(self, request):
        try:
            bot_to_start_model = bot.ChangeStatusRequestBody.parse_obj(request.data)
        except ValidationError as error:
            return Response(data={'success': False,
                                  'error_message': str(error)}, content_type='application/json', status=400)

        bot_id = bot_to_start_model.bot_id
        bot_db = Bot.objects.get(pk=bot_id)

        if bot_db.status != 'enabled':
            bot_db.status = 'enabled'
            bot_db.save()

        return Response(data={'success': True}, content_type='application/json')


class BotStoppingView(APIView):
    def patch(self, request):
        try:
            bot_to_stop_model = bot.ChangeStatusRequestBody.parse_obj(request.data)
        except ValidationError as error:
            return Response(data={'success': False,
                                  'error_message': str(error)}, content_type='application/json', status=400)

        bot_id = bot_to_stop_model.bot_id
        bot_db = Bot.objects.get(pk=bot_id)

        if bot_db.status != 'disabled':
            bot_db.status = 'disabled'
            bot_db.save()

        return Response(data={'success': True}, content_type='application/json')


class BotDeletingView(APIView):
    def patch(self, request):
        try:
            bot_to_delete_model = bot.ChangeStatusRequestBody.parse_obj(request.data)
        except ValidationError as error:
            return Response(data={'success': False,
                                  'error_message': str(error)}, content_type='application/json', status=400)

        bot_id = bot_to_delete_model.bot_id
        bot_db = Bot.objects.get(pk=bot_id)
        bot_db.delete()

        return Response(data={'success': True}, content_type='application/json')


class BotInfoView(APIView):
    def get(self, request):
        try:
            bot_model = bot.ChangeStatusRequestBody.parse_obj(request.data)
        except ValidationError as error:
            return Response(data={'success': False,
                                  'error_message': str(error)}, content_type='application/json', status=400)

        # TODO: add bot and user validating
        # TODO: need to generalize tracker mechanisms
        bot_db = Bot.objects.get(pk=bot_model.id)
        bot_json = {'name': bot_db.name, 'bot_id': bot_model.id, 'type': bot_db.type, 'status': bot_db.status,
                    'condition': bot_db.condition, 'schedule': bot_db.schedule, 'traffic_source': bot_db.traffic_source,
                    'ts_api_key': bot_db.ts_api_key, 'tracker': bot_db.tracker,
                    'tracker_api_key': bot_db.tracker_api_key,
                    'campaigns_ids': bot_db.campaigns_list, 'user_id': bot_db.user_id, 'period': bot_db.period,
                    'action': bot_db.action,
                    'ignored_sources': bot_db.ignored_sources}

        return Response(data={'success': True, 'info': bot_json}, content_type='application/json',
                        status=200)


class BotListView(APIView):
    def get(self, request):
        pass
