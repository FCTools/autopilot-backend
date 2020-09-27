"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""
import json

import requests
from django.conf import settings

from bot_manager.services.helpers import requests_manager
from bot_manager.models import User


class Updater:
    def __init__(self):
        pass

    def _update_offers(self):
        pass

    def _update_campaigns(self):
        pass

    def _update_users(self):
        """
        Gets users from tracker.

        :return: list of users
        :rtype: List[User]
        """

        response = requests_manager.get(
            requests.Session(), settings.TRACKER_URL, params={"page": "Users", "api_key": settings.BINOM_API_KEY}
        )

        if not isinstance(response, requests.Response):
            return

        try:
            response_json = response.json()
        except json.JSONDecodeError as decode_error:
            return

        try:
            users_list = [User(id=int(user["id"]), login=user["login"]) for user in response_json]

        except KeyError:
            return

        users_db = User.objects.all()

        for user in users_list:
            if user not in users_db:
                user.save()

    def _update_traffic_sources(self):
        pass

    def update(self):
        self._update_users()
        self._update_offers()
        self._update_traffic_sources()
        self._update_campaigns()
