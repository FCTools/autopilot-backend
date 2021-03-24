# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

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

        new_bot_db = Bot.objects.create(name=new_bot.name,
                                        type=new_bot.type,
                                        user_id=new_bot.user_id,
                                        traffic_source=ts,
                                        condition=new_bot.condition,
                                        status='disabled',
                                        action=new_bot.action,
                                        ts_api_key=new_bot.ts_api_key,
                                        schedule=new_bot.schedule,
                                        period=new_bot.period,
                                        ignored_zones=new_bot.ignored_sources, )

        # for campaign in new_bot.campaigns_ids:
        #     new_bot_db.campaigns.add(campaign.)

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

        Bot.objects.get(pk=bot_to_update.bot_id).update(name=bot_to_update.name,
                                                        type=bot_to_update.type,
                                                        user_id=bot_to_update.user_id,
                                                        traffic_source=ts,
                                                        condition=bot_to_update.condition,
                                                        status='disabled',
                                                        action=bot_to_update.action,
                                                        ts_api_key=bot_to_update.ts_api_key,
                                                        schedule=bot_to_update.schedule,
                                                        period=bot_to_update.period,
                                                        ignored_zones=bot_to_update.ignored_sources, )

        # TODO: add campaigns updating
        # for campaign in new_bot.campaigns_ids:
        #     new_bot_db.campaigns.add(campaign.)

        return Response(data={'success': True}, content_type='application/json')
