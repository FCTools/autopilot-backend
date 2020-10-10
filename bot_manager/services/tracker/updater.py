"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""
import json
from copy import deepcopy
from urllib.parse import urlencode

import requests
from django.conf import settings

from bot_manager.models import User, Offer, TrafficSource, Campaign
from bot_manager.services.helpers import requests_manager


class Updater:
    @staticmethod
    def _update_offers():
        """
        Gets offers from tracker.

        :return: list of offers
        :rtype: List[Offer]
        """

        response = requests_manager.get(
            requests.Session(),
            settings.TRACKER_URL,
            params={"page": "Offers", "api_key": settings.BINOM_API_KEY, "group": "all", "status": "all"},
        )

        if not isinstance(response, requests.Response):
            return

        try:
            response_json = response.json()
        except json.JSONDecodeError as decode_error:
            return

        try:
            offers_list = [
                Offer(
                    id=int(offer["id"]),
                    geo=offer["geo"],
                    name=offer["name"],
                    group=offer["group_name"],
                    network=offer["network_name"],
                )
                for offer in response_json
            ]

        except KeyError:
            return

        offers_db = Offer.objects.all()

        for offer in offers_list:
            if offer not in offers_db:
                offer.save()

    @staticmethod
    def _get_offers_ids_by_campaign(campaign_id):
        result = []

        requests_url = settings.TRACKER_URL + "arm.php"
        response = requests_manager.get(
            requests.Session(),
            requests_url,
            params={
                "page": "Campaigns",
                "api_key": settings.BINOM_API_KEY,
                "action": "campaign@get_full",
                "id": campaign_id,
            },
        )

        if not isinstance(response, requests.Response):
            return []

        try:
            response_json = response.json()
        except json.JSONDecodeError as decode_error:
            return []

        try:
            for path in response_json["routing"]["paths"]:
                result += [int(offer["id_t"]) for offer in path["offers"]]
        except KeyError:
            return []

        return result

    @staticmethod
    def _update_campaigns():
        users_db = User.objects.all()
        campaigns_list = []

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

        all_campaigns_tracker_number = len(all_campaigns_tracker_json)
        added_campaigns_ids = []

        for user in users_db:
            params = {
                "page": "Campaigns",
                "user_group": user.id,
                "status": "all",
                "api_key": settings.BINOM_API_KEY,
            }

            campaigns_tracker = requests_manager.get(
                requests.Session(), f"{settings.TRACKER_URL}?timezone=+3:00&{urlencode(params)}"
            )

            if not isinstance(campaigns_tracker, requests.Response):
                return

            try:
                campaigns_tracker_json = campaigns_tracker.json()
            except json.JSONDecodeError as decode_error:
                return

            if not campaigns_tracker_json:
                continue

            if len(campaigns_tracker_json) == all_campaigns_tracker_number:
                continue

            campaigns_to_add = []

            for campaign in campaigns_tracker_json:
                campaign_db = Campaign.objects.filter(id__exact=campaign['id'])
                if not campaign_db:
                    campaigns_to_add.append(deepcopy(campaign))
                    added_campaigns_ids.append(campaign['id'])

            try:
                result = [
                    {
                        "instance": Campaign(
                            id=int(campaign["id"]),
                            name=campaign["name"],
                            traffic_group=campaign["group_name"],
                            traffic_source_id=int(campaign["ts_id"]),
                            user=user,
                            status=None,
                        ),
                        "offers_list": [],
                    }
                    for campaign in campaigns_to_add
                ]
            except KeyError:
                return

            for campaign in all_campaigns_tracker_json:
                if campaign['id'] not in added_campaigns_ids:
                    result.append({
                        "instance": Campaign(
                            id=int(campaign["id"]),
                            name=campaign["name"],
                            traffic_group=campaign["group_name"],
                            traffic_source_id=int(campaign["ts_id"]),
                            user_id=-1,
                            status=None,
                        ),
                        "offers_list": [],
                    })

            for campaign in result:
                offers_ids = Updater._get_offers_ids_by_campaign(campaign["instance"].id)

                if not offers_ids:
                    return

                campaign["offers_list"] = offers_ids

            campaigns_list += result

        for campaign in campaigns_list:
            in_db = Campaign.objects.filter(id__exact=campaign['instance'].id)

            if not in_db:
                campaign['instance'].save()

                for offer_id in campaign['offers_list']:
                    offer = Offer.objects.get(id__exact=offer_id)
                    campaign['instance'].offers_list.add(offer)

                campaign['instance'].save()

    @staticmethod
    def _update_users():
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

    @staticmethod
    def _update_traffic_sources():
        """
        Gets traffic sources from tracker.

        :return: list of traffic sources
        :rtype: List[TrafficSource]
        """

        session = requests.Session()
        result = []

        all_traffic_sources = requests_manager.get(
            session,
            settings.TRACKER_URL,
            params={"page": "Traffic_Sources", "api_key": settings.BINOM_API_KEY, "status": "all"},
        )

        if not isinstance(all_traffic_sources, requests.Response):
            return

        try:
            all_traffic_sources_number = len(all_traffic_sources.json())
        except json.JSONDecodeError as decode_error:
            return

        for user in User.objects.all():
            user_traffic_sources = requests_manager.get(
                session,
                settings.TRACKER_URL,
                params={
                    "page": "Traffic_Sources",
                    "api_key": settings.BINOM_API_KEY,
                    "user_group": user.id,
                    "status": "all",
                },
            )

            if not isinstance(user_traffic_sources, requests.Response):
                continue

            try:
                user_traffic_sources_json = user_traffic_sources.json()
            except json.JSONDecodeError as decode_error:
                return

            if user_traffic_sources_json and len(user_traffic_sources_json) != all_traffic_sources_number:
                try:
                    result += [
                        TrafficSource(
                            id=int(traffic_source["id"]),
                            name=traffic_source["name"],
                            campaigns=int(traffic_source["camps"]),
                            tokens=1 if int(traffic_source["tokens"]) else 0,
                            user=user,
                        )
                        for traffic_source in user_traffic_sources_json
                    ]
                except KeyError:
                    return

        traffic_sources_db = TrafficSource.objects.all()

        for traffic_source in result:
            if traffic_source not in traffic_sources_db:
                traffic_source.save()

    @staticmethod
    def update():
        Updater._update_users()
        Updater._update_offers()
        Updater._update_traffic_sources()
        Updater._update_campaigns()
