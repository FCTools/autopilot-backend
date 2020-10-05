"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

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

AVAILABLE_ACTIONS = ("stop_campaign", "start_campaign", "add_to_bl", "add_to_wl")


class BotCreator(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()

    # handling bots/createBot is here
    def post(self, request, format=None):
        permission_classes = [IsAuthenticated]

        # custom logic start
        # print(ConditionParser.check_sites("(((revenue < 50) AND (profit < 0)) OR (cost > 100))", 1379))
        # custom logic end

        validator = Validator
        validation_status, error_message = validator.validate_new_bot(request.data)

        if validation_status is True:
            name = request.data.get('name')
            bot_type = int(request.data.get('type'))
            condition = request.data.get('condition')
            action = int(request.data.get('action'))
            user_id = int(request.data.get('user_id'))
            campaigns_ids = [int(camp_id) for camp_id in request.data.get('campaigns_ids')]
            period = int(request.data.get('period'))
            schedule = parse_schedule(request.data.get('schedule'))

            if bot_type == 1 and 'ignored_sources' in request.data:
                ignored_sources = request.data.get('ignored_sources')

            # how to remember ignored sources?
            new_bot = Bot.objects.create(name=name, type=bot_type, condition=condition, action=action, user_id=user_id,
                                         period=period, schedule=schedule, )

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

        bot.status = "disabled"
        bot.save()

        return Response(data={'status': True},
                        content_type='application/json')


class BotDeleter(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()

    def delete(self, request):
        if 'bot_id' in request.data:
            bot_id = request.data.get('bot_id')
        else:
            return Response(data={'success': False, 'error': 'bot_id field is required'},
                            content_type='application/json')

        try:
            bot = get_object_or_404(Bot, pk=bot_id)
        except Http404:
            return Response(data={'status': False, 'error': "bot with given id doesn't exist"},
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

        validator = Validator
        validation_status, error_message = validator.validate_new_bot(request.data, bot_exists=True)

        if validation_status is True:
            bot.name = request.data.get('name')
            bot.type = request.data.get('type')
            bot.condition = request.data.get('condition')
            bot.action = request.data.get('action')
            bot.interval = request.data.get('checking_interval')

            bot.save()

            campaigns_ids = request.data.get('campaigns_ids')

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

            # how to remember ignored sources?

            bot.save()

            return Response(data={'status': True}, content_type='application/json')
        else:
            return Response(data={'status': False, 'error': error_message},
                            content_type='application/json')
