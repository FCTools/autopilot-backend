"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""
import json

from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from bot_manager.domains.accounts.bot import Bot
from bot_manager.serializers import BotSerializer
from bot_manager.services.tracker.updater import Updater
from bot_manager.models import User, Campaign


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
            return Response(data={'success': False, 'error': 'user_id is required'},
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

    def get(self, request, pk):
        """
        Return a list of all user's bots.
        """
        permission_classes = [IsAuthenticated]
        bot = get_object_or_404(Bot, pk=pk)
        data = BotSerializer(bot).data
        return Response(data)


class BotCreator(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()

    # handling bots/createBot is here
    def post(self, request, format=None):
        permission_classes = [IsAuthenticated]
        updated = False

        if 'name' in request.data:
            name = request.data.get('name')

            if len(name) == 0:
                return Response(data={'success': False, 'error': "name field can't be empty"},
                                content_type='application/json')
            elif len(name) > 128:
                return Response(data={'success': False, 'error': "too long name (max: 120 symbols)"},
                                content_type='application/json')
        else:
            return Response(data={'success': False, 'error': 'name field is required'},
                            content_type='application/json')

        if 'type' in request.data:
            try:
                bot_type = int(request.data.get('type'))
            except ValueError:
                return Response(data={'success': False, 'error': 'invalid bot type - not a number'},
                                content_type='application/json')

            if bot_type != 1 and bot_type != 2:
                return Response(data={'success': False, 'error': 'bot type can be only 1 or 2'},
                                content_type='application/json')
        else:
            return Response(data={'success': False, 'error': 'type field is required'},
                            content_type='application/json')

        if 'condition' in request.data:
            condition = request.data.get('condition')
        else:
            return Response(data={'success': False, 'error': 'condition field is required'},
                            content_type='application/json')

        if 'action' in request.data:
            action = request.data.get('action')

            if action not in AVAILABLE_ACTIONS:
                return Response(data={'success': False, 'error': 'invalid action'},
                                content_type='application/json')
        else:
            return Response(data={'success': False, 'error': 'action field is required'},
                            content_type='application/json')

        if 'interval' in request.data:
            interval = request.data.get('interval')

            if interval < 120:
                return Response(data={'success': False, 'error': "checking interval can't be less than 120 seconds"},
                                content_type='application/json')
        else:
            return Response(data={'success': False, 'error': 'interval field is required'},
                            content_type='application/json')

        if bot_type == 1:
            if 'list_type' in request.data:
                list_type = request.data.get('list_type')

                if list_type == 'black':
                    list_type = 1
                elif list_type == 'white':
                    list_type = 0
                else:
                    return Response(data={'success': False, 'error': 'invalid list type'},
                                    content_type='application/json')
            else:
                return Response(data={'success': False, 'error': 'list_type is required for bots of type 1'},
                                content_type='application/json')
        else:
            list_type = None

        if 'user_id' in request.data:
            user_id = request.data.get('user_id')
            user = list(User.objects.filter(id__exact=user_id))

            if not user:
                Updater.update()
                updated = True

            user = list(User.objects.filter(id__exact=user_id))

            if not user:
                return Response(data={'success': False, 'error': 'unknown user'},
                                content_type='application/json')

        else:
            return Response(data={'success': False, 'error': 'user_id field is required'},
                            content_type='application/json')

        if 'campaigns' in request.data:
            campaigns_ids = request.data.get('campaigns')

            for campaign_id in campaigns_ids:
                campaign_db = list(Campaign.objects.filter(id__exact=campaign_id))

                if not campaign_db:
                    if not updated:
                        Updater.update()
                        updated = True
                    else:
                        return Response(data={'success': False, 'error': f'unknown campaign: {campaign_id}'},
                                        content_type='application/json')

                campaign_db = list(Campaign.objects.filter(id__exact=campaign_id))

                if not campaign_db:
                    return Response(data={'success': False, 'error': f'unknown campaign: {campaign_id}'},
                                    content_type='application/json')

                campaign = campaign_db[0]
                if campaign.user_id != user_id:
                    return Response(data={'success': False, 'error': f'campaign {campaign_id} pinned to another user'},
                                    content_type='application/json')

        else:
            return Response(data={'success': False, 'error': 'campaigns field is required'},
                            content_type='application/json')

        user_bots = Bot.objects.filter(user_id=user_id)

        for bot in user_bots:
            if bot.name == name:
                return Response(data={'success': False, 'error': 'this user already has bot with this name'},
                                content_type='application/json')

        new_bot = Bot.objects.create(name=name, type=bot_type, condition=condition, action=action,
                                     checking_interval=interval, user_id=user_id, list_type=list_type)

        for campaign_id in campaigns_ids:
            campaign = Campaign.objects.get(id__exact=campaign_id)
            new_bot.campaigns_list.add(campaign)

        new_bot.save()

        return Response(data={'success': True, 'bot_id': new_bot.id},
                        content_type='application/json')


class BotStarter(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()

    def post(self, request):
        if 'bot_id' in request.data:
            bot_id = request.data.get('bot_id')
        else:
            return Response(data={'success': False, 'error': 'bot id is required'},
                            content_type='application/json')

        bot = get_object_or_404(Bot, pk=bot_id)
        bot.status = "enabled"
        bot.save()

        return Response(data={'success': True},
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

        bot = get_object_or_404(Bot, pk=bot_id)
        bot.delete()

        return Response(data={'success': True},
                        content_type='application/json')


class BotUpdater(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()

    def post(self, request):
        pass
