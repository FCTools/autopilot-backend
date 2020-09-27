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
