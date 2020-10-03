"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""
from pprint import pprint

import requests

from bot_manager.services.helpers import requests_manager
from django.conf import settings
from bot_manager.models import Campaign


class TrackerManager:
    def __init__(self):
        pass

    def get_campaign_info(self, campaign):
        pass

    def analyse_sites(self, campaign_id, condition):
        pass

    def get_sites_info(self, campaign_id):
        campaign = Campaign.objects.get(pk=campaign_id)
        group_1 = campaign.traffic_source.filtering_param_number

        campaign_sites_info = requests_manager.get(requests.Session(), settings.TRACKER_URL,
                                                   params={
                                                       'api_key': settings.BINOM_API_KEY,
                                                       'page': 'Stats',
                                                       'camp_id': campaign_id,
                                                       'group1': group_1,
                                                       'group2': 1,
                                                       'group3': 1,
                                                       'date': 1,
                                                   }).json()

        return campaign_sites_info

    def get_campaign_info(self, campaign_id):
        requests_url = settings.TRACKER_URL
        response = requests_manager.get(
            requests.Session(),
            requests_url,
            params={
                "page": "Stats",
                "api_key": settings.BINOM_API_KEY,
                "camp_id": campaign_id,
                "group1": 3,
                "group2": 1,
                "group3": 1
            },
        ).json()

        pprint(response)
        return response


TrackerManager().get_campaign_info(1903)
