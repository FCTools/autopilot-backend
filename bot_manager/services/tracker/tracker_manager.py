"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""
from datetime import datetime, timedelta
from urllib.parse import urlencode

import requests
from django.conf import settings

from bot_manager.models import Campaign
from bot_manager.services.helpers import requests_manager


class TrackerManager:
    def __init__(self):
        pass

    def analyse_sites(self, campaign_id, condition):
        pass

    def get_sites_info(self, campaign_id, period):
        campaign = Campaign.objects.get(pk=campaign_id)
        group_1 = campaign.traffic_source.filtering_param_number_sources
        now = datetime.utcnow()
        end_time = datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute)
        start_time = end_time - timedelta(minutes=period)

        campaign_sites_info = requests_manager.get(requests.Session(), settings.TRACKER_URL,
                                                   params={
                                                       'page': 'Stats',
                                                       'camp_id': campaign_id,
                                                       'group1': group_1,
                                                       'group2': 1,
                                                       'group3': 1,
                                                       'date': 10,
                                                       "date_s": start_time.strftime("%Y-%m-%d %I:%M"),
                                                       "date_e": end_time.strftime("%Y-%m-%d %I:%M"),
                                                       "timezone": "+3:00",
                                                       'api_key': settings.BINOM_API_KEY
                                                   }).json()

        return campaign_sites_info

    # period in minutes
    def get_campaign_info(self, campaign_id, period):
        now = datetime.utcnow()
        end_time = datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute)
        start_time = end_time - timedelta(minutes=period)

        group1 = Campaign.objects.get(id__exact=campaign_id).traffic_source.filtering_param_number_campaigns

        requests_url = settings.TRACKER_URL
        response = requests_manager.get(
            requests.Session(),
            requests_url,
            params={
                "page": "Stats",
                "api_key": settings.BINOM_API_KEY,
                "camp_id": campaign_id,
                "group1": group1,
                "group2": 1,
                "group3": 1,
                "date": 10,
                "date_e": end_time.strftime("%Y-%m-%d+%I:%M"),
                "date_s": start_time.strftime("%Y-%m-%d+%I:%M")
            },
        ).json()

        return response
