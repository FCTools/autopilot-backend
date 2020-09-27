"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from bot_manager.domains.accounts.bot import Bot
from bot_manager.serializers import BotSerializer
from bot_manager.services.tracker.updater import Updater


class ListBots(APIView):
    """
    View to list all user bots in the system.

    * Requires token authentication.
    """

    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()
    serializer = BotSerializer

    def get(self, request, format=None):
        """
        Return a list of all user's bots.
        """
        permission_classes = [IsAuthenticated]

        names = [bot.name for bot in Bot.objects.all()]
        return Response(names)


class BotCreator(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Bot.objects.all()

    # handling bots/createBot is here
    def post(self, request, format=None):
        Updater.update()

        permission_classes = [IsAuthenticated]

        if 'name' in request.data:
            name = request.data.get('name')

            if len(name) == 0:
                # name can't be empty
                pass
            elif len(name) > 128:
                # too long name
                pass
        else:
            # name field is required
            pass

        if 'type' in request.data:
            try:
                type = int(request.data.get('type'))
            except TypeError:
                # Invalid bot type - not a number
                pass

            if type != 1 and type != 2:
                # Invalid bot type: type can be only 1 or 2
                pass
        else:
            # bot type field is required
            pass



        names = [bot.name for bot in Bot.objects.all()]
        return Response("Something happened!")
