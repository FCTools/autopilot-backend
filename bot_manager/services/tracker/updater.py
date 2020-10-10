"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

import json
from urllib.parse import urlencode

import requests
from django.conf import settings

from bot_manager.models import TrafficSource, Campaign
from bot_manager.services.helpers import requests_manager


class Updater:
    @staticmethod
    def _update_campaigns():
        params = {
            "page": "Campaigns",
            "status": "all",
            "api_key": settings.BINOM_API_KEY,
        }

        all_campaigns_tracker = requests_manager.get(
            requests.Session(), f"{settings.TRACKER_URL}?timezone=+3:00&{urlencode(params)}"
        )

        if not isinstance(all_campaigns_tracker, requests.Response):
            return

        try:
            all_campaigns_tracker_json = all_campaigns_tracker.json()
        except json.JSONDecodeError as decode_error:
            return

        campaigns_db_ids = [campaign.id for campaign in Campaign.objects.all()]

        for campaign in all_campaigns_tracker_json:
            if campaign["id"] not in campaigns_db_ids:
                Campaign.objects.create(id=int(campaign["id"]),
                                        name=campaign["name"],
                                        traffic_group=campaign["group_name"],
                                        traffic_source_id=int(campaign["ts_id"]),
                                        status=None)

    @staticmethod
    def _update_traffic_sources():
        """
        Get traffic sources from tracker.

        :return: list of traffic sources
        :rtype: List[TrafficSource]
        """

        session = requests.Session()

        all_traffic_sources = requests_manager.get(
            session,
            settings.TRACKER_URL,
            params={"page": "Traffic_Sources", "api_key": settings.BINOM_API_KEY, "status": "all"},
        )

        if not isinstance(all_traffic_sources, requests.Response):
            return

        try:
            all_traffic_sources_json = all_traffic_sources.json()
        except json.JSONDecodeError as decode_error:
            return

        traffic_sources_db_ids = [ts.id for ts in TrafficSource.objects.all()]

        for traffic_source in all_traffic_sources_json:
            if traffic_source["id"] not in traffic_sources_db_ids:
                TrafficSource.objects.create(id=int(traffic_source["id"]),
                                             name=traffic_source["name"])

    @staticmethod
    def update():
        Updater._update_traffic_sources()
        Updater._update_campaigns()
