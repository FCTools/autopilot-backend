# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import json

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bot_manager.domains.accounts.bot import Bot
from bot_manager.models import Campaign
from bot_manager.services.helpers.parse_schedule import parse_schedule
from bot_manager.services.helpers.validator import Validator


class BotCreator(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()

    # handling bots/createBot is here
    def post(self, request, format=None):
        permission_classes = [IsAuthenticated]

        validator = Validator
        validation_status, error_message = validator.validate_new_bot(request.data)

        if validation_status is True:
            name = request.data.get('name')
            bot_type = int(request.data.get('type'))
            condition = request.data.get('condition')
            action = int(request.data.get('action'))
            user_id = int(request.data.get('user_id'))
            period = int(request.data.get('period'))
            schedule = parse_schedule(request.data.get('schedule'))

            if 'AND' not in condition and 'OR' not in condition:
                condition = condition[1:-1]

            if bot_type == 1 and 'ignored_sources' in request.data:
                ignored_sources = request.data.get('ignored_sources')
            else:
                ignored_sources = []

            source_info = []

            for campaign in request.data.get('campaigns_ids'):
                source_info.append({'tracker_id': int(campaign['tracker_id']), 'source_id': campaign['source_id'],
                                    'status': 'started'})

            new_bot = Bot.objects.create(name=name, type=bot_type, condition=condition, action=action, user=user_id,
                                         period=period, schedule=schedule, ignored_sources=json.dumps(ignored_sources),
                                         source_info=json.dumps(source_info))

            campaigns_ids = set([int(campaign['tracker_id']) for campaign in source_info])

            for campaign_id in campaigns_ids:
                campaign = Campaign.objects.get(id__exact=campaign_id)
                new_bot.campaigns_list.add(campaign)

            new_bot.save()

            return Response(data={'status': True, 'bot_id': new_bot.id},
                            content_type='application/json')
        else:
            return Response(data={'status': False, 'error': error_message},
                            content_type='application/json')


class BotStarter(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()

    def patch(self, request):
        if 'bot_id' in request.data:
            bot_id = request.data.get('bot_id')
        else:
            return Response(data={'status': False, 'error': 'bot_id field is required'},
                            content_type='application/json')

        try:
            bot = get_object_or_404(Bot, pk=bot_id)
        except Http404:
            return Response(data={'status': False, 'error': "bot with given id doesn't exist"},
                            content_type='application/json')

        if 'user_id' in request.data:
            if int(request.data.get('user_id')) != bot.user:
                return Response(data={'status': False, 'error': "invalid user_id"},
                                content_type='application/json')
        else:
            return Response(data={'status': False, 'error': "user_id is required"},
                            content_type='application/json')

        bot.status = "enabled"
        bot.save()

        return Response(data={'status': True}, content_type='application/json')


class BotStopper(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()

    def patch(self, request):
        if 'bot_id' in request.data:
            bot_id = request.data.get('bot_id')
        else:
            return Response(data={'status': False, 'error': 'bot_id field is required'},
                            content_type='application/json')

        try:
            bot = get_object_or_404(Bot, pk=bot_id)
        except Http404:
            return Response(data={'status': False, 'error': "bot with given id doesn't exist"},
                            content_type='application/json')

        if 'user_id' in request.data:
            if int(request.data.get('user_id')) != bot.user:
                return Response(data={'status': False, 'error': "invalid user_id"},
                                content_type='application/json')
        else:
            return Response(data={'status': False, 'error': "user_id is required"},
                            content_type='application/json')

        bot.status = "disabled"
        bot.save()

        return Response(data={'status': True},
                        content_type='application/json')


class BotDeleter(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()

    def patch(self, request):
        if 'bot_id' in request.data:
            bot_id = request.data.get('bot_id')
        else:
            return Response(data={'status': False, 'error': 'bot_id field is required'},
                            content_type='application/json')

        try:
            bot = get_object_or_404(Bot, pk=bot_id)
        except Http404:
            return Response(data={'status': False, 'error': "bot with given id doesn't exist"},
                            content_type='application/json')

        if 'user_id' in request.data:
            if int(request.data.get('user_id')) != bot.user:
                return Response(data={'status': False, 'error': "invalid user_id"},
                                content_type='application/json')
        else:
            return Response(data={'status': False, 'error': "user_id is required"},
                            content_type='application/json')

        bot.delete()

        return Response(data={'status': True}, content_type='application/json')


class BotUpdater(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()

    def put(self, request):
        permission_classes = [IsAuthenticated]

        if 'bot_id' in request.data:
            bot_id = request.data.get('bot_id')

            try:
                bot = get_object_or_404(Bot, pk=bot_id)
            except Http404:
                return Response(data={'status': False, 'error': "bot with given id doesn't exist"},
                                content_type='application/json')
        else:
            return Response(data={'status': False, 'error': "bot_id field is required"},
                            content_type='application/json')

        if bot.status == "enabled":
            return Response(data={'status': False, 'error': "can't change enabled bot"},
                            content_type='application/json')

        validator = Validator
        validation_status, error_message = validator.validate_new_bot(request.data, bot_exists=True,
                                                                      user_id=bot.user)

        if validation_status is True:
            bot_name = request.data.get('name')
            bot_type = int(request.data.get('type'))
            bot_condition = request.data.get('condition')
            bot_action = int(request.data.get('action'))
            bot_schedule = parse_schedule(request.data.get('schedule'))
            bot_period = int(request.data.get('period'))

            if 'AND' not in bot_condition and 'OR' not in bot_condition:
                bot_condition = bot_condition[1:-1]

            if bot_type == 1 and bot_action != bot.action:
                return Response(data={'status': False, 'error': "changing list type is not allowed"},
                                content_type='application/json')

            bot.name = bot_name
            bot.type = bot_type
            bot.condition = bot_condition
            bot.schedule = bot_schedule
            bot.period = bot_period

            bot.save()

            campaigns_ids = [int(camp_id['tracker_id']) for camp_id in request.data.get('campaigns_ids')]

            for campaign in bot.campaigns_list.all():
                if campaign.id not in campaigns_ids:
                    bot.campaigns_list.remove(campaign)

            for campaign_id in campaigns_ids:
                campaign = Campaign.objects.get(id__exact=campaign_id)

                if campaign not in bot.campaigns_list.all():
                    bot.campaigns_list.add(campaign)

            bot.save()

            if bot.type == 1 and 'ignored_sources' in request.data:
                ignored_sources = request.data.get('ignored_sources')
                bot.ignored_sources = ignored_sources

            source_info = []

            if bot.type == 2:
                for campaign in request.data.get('campaigns_ids'):
                    source_info.append({'tracker_id': int(campaign['tracker_id']), 'source_id': campaign['source_id'],
                                        'status': 'started'})

            bot.source_info = json.dumps(source_info)

            bot.status = "enabled"
            bot.save()

            return Response(data={'status': True}, content_type='application/json')
        else:
            return Response(data={'status': False, 'error': error_message},
                            content_type='application/json')
