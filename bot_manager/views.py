"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication

from bot_manager.domains.accounts.bot import Bot
from bot_manager.serializers import BotSerializer
from bot_manager.services.tracker.updater import Updater
from bot_manager.models import User, Campaign
from bot_manager.services.helpers.validator import Validator

AVAILABLE_ACTIONS = ("stop_campaign", "start_campaign", "add_to_bl", "add_to_wl")


class ListBots(APIView):
    """
    View to list all user bots in the system.

    * Requires token authentication.
    """

    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()
    serializer = BotSerializer

    def get(self, request):
        """
        Return a list of all user's bots.
        """
        permission_classes = [IsAuthenticated]
        if 'user_id' not in request.data:
            return Response(data={'status': False, 'error': 'user_id is required'},
                            content_type='application/json')

        user_id = request.data.get('user_id')

        bots = Bot.objects.filter(user_id__exact=user_id)

        data = BotSerializer(bots, many=True)
        return Response(data.data)


class BotDetail(APIView):
    """
    View to list all user bots in the system.

    * Requires token authentication.
    """

    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()
    serializer = BotSerializer

    def get(self, request):
        """
        Return a list of all user's bots.
        """
        permission_classes = [IsAuthenticated]

        if 'bot_id' in request.data:
            bot_id = request.data.get('bot_id')
        else:
            return Response(data={'status': False, 'error': 'bot id is required'},
                            content_type='application/json')

        try:
            bot = get_object_or_404(Bot, pk=bot_id)
        except Http404:
            return Response(data={'status': False, 'error': f"can't find bot with id {bot_id}"},
                            content_type='application/json')

        data = BotSerializer(bot).data
        return Response(data)


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
            bot_type = request.data.get('type')
            condition = request.data.get('condition')
            action = request.data.get('action')
            interval = request.data.get('checking_interval')
            user_id = request.data.get('user_id')
            campaigns_ids = request.data.get('campaigns_ids')

            if bot_type == 1 and 'ignored_sources' in request.data:
                ignored_sources = request.data.get('ignored_sources')

            new_bot = Bot.objects.create(name=name, type=bot_type, condition=condition, action=action,
                                         checking_interval=interval, user_id=user_id, list_type=list_type)

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

    def post(self, request):
        if 'bot_id' in request.data:
            bot_id = request.data.get('bot_id')
        else:
            return Response(data={'status': False, 'error': 'bot id is required'},
                            content_type='application/json')

        bot = get_object_or_404(Bot, pk=bot_id)
        bot.status = "enabled"
        bot.save()

        return Response(data={'status': True},
                        content_type='application/json')


class BotStopper(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()

    def post(self, request):
        if 'bot_id' in request.data:
            bot_id = request.data.get('bot_id')
        else:
            return Response(data={'success': False, 'error': 'bot id is required'},
                            content_type='application/json')

        bot = get_object_or_404(Bot, pk=bot_id)
        bot.status = "disabled"
        bot.save()

        return Response(data={'success': True},
                        content_type='application/json')


class BotDeleter(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()

    def delete(self, request):
        if 'bot_id' in request.data:
            bot_id = request.data.get('bot_id')
        else:
            return Response(data={'success': False, 'error': 'bot id is required'},
                            content_type='application/json')

        try:
            bot = get_object_or_404(Bot, pk=bot_id)
        except Http404:
            return Response(data={'status': False, 'error': f"can't find bot with id {bot_id}"},
                            content_type='application/json')

        bot.delete()

        return Response(data={'success': True},
                        content_type='application/json')


class BotUpdater(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()

    def post(self, request):
        pass
