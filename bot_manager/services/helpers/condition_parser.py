"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from copy import deepcopy

from bot_manager.domains.tracker.campaign import Campaign
from bot_manager.domains.tracker.site import Site
from bot_manager.services.tracker.tracker_manager import TrackerManager

AVAILABLE_SYMBOLS = ['(', ')', '>', '<', '=', '<=', '>=', 'OR', 'AND',
                     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-']
AVAILABLE_VARIABLES = ['revenue', 'cost', 'profit', 'clicks', 'CPC', 'ROI', 'CR', 'EPC', 'leads', 'cpa', 'approve_%']


class ConditionParser:
    @staticmethod
    def bracket_sequence_is_valid(condition):
        if condition[0] != '(' or condition[-1] != ')':
            return False

        counter = 0

        bracket_sequence = [symbol for symbol in list(deepcopy(condition)[1:-1]) if symbol in ['(', ')']]

        for bracket in bracket_sequence:
            if bracket == '(':
                counter += 1
            else:
                counter -= 1

            if counter < 0:
                return False

        return counter == 0

    @staticmethod
    def _all_symbols_is_correct(condition):
        condition_copy = deepcopy(condition)

        for symbol in AVAILABLE_SYMBOLS:
            condition_copy = condition_copy.replace(symbol, '')
        for variable in AVAILABLE_VARIABLES:
            condition_copy = condition_copy.replace(variable, '')

        return len(condition_copy.replace(' ', '')) == 0

    @staticmethod
    def _split_into_parts(condition):
        condition_copy = deepcopy(condition)

        tokens = list(condition_copy)
        first_condition_end = 0

        counter = 0
        for n, symbol in enumerate(tokens):
            if symbol == '(':
                counter += 1
            elif symbol == ')':
                counter -= 1

            if counter == 0:
                first_condition_end = n
                break

        first_part = condition_copy[:first_condition_end + 1]
        conn = condition_copy[first_condition_end + 1:].strip().split()[0]
        second_part = condition_copy[first_condition_end + 3 + len(conn):]

        return first_part, conn, second_part

    @staticmethod
    def _check_site_elementary_condition(site_info, condition):
        parts = condition[1:-1].split()

        var = parts[0].lower()
        relation = parts[1]
        value = float(parts[2])

        if relation == '=':
            return float(site_info[var]) == value
        elif relation == '<':
            return float(site_info[var]) < value
        elif relation == '<=':
            return float(site_info[var]) <= value
        elif relation == '>':
            return float(site_info[var]) > value
        else:
            return float(site_info[var]) >= value

    @staticmethod
    def check_site_condition(site_info, condition):
        if 'OR' not in condition and 'AND' not in condition:
            return ConditionParser._check_site_elementary_condition(site_info, condition)

        condition = condition[1:-1]

        first_cond, conn, second_cond = ConditionParser._split_into_parts(condition)

        if conn == 'AND':
            return ConditionParser.check_site_condition(site_info, first_cond) and \
                   ConditionParser.check_site_condition(site_info, second_cond)
        else:
            return ConditionParser.check_site_condition(site_info, first_cond) or \
                   ConditionParser.check_site_condition(site_info, second_cond)

    @staticmethod
    def check_sites(condition, campaign_id, period, action):
        if not ConditionParser.is_valid(condition):
            return

        sites_to_add = []

        sites_db = list(Site.objects.filter(campaign_id=campaign_id))
        sites_db_ids = [site.site_id for site in sites_db]

        sites = TrackerManager().get_sites_info(campaign_id, period)
        print(sites)
        if not sites:
            return []

        print(condition)

        for site in sites:
            if site['name'] in sites_db_ids:
                site_db = sites_db[sites_db_ids.index(site['name'])]
                if site_db.status == action:
                    continue

            if ConditionParser.check_site_condition(site, condition):
                sites_to_add.append(site['name'])
                Site.objects.create(campaign_id=campaign_id, site_id=site['name'], name=None, status=action)

        return sites_to_add

    @staticmethod
    def _check_campaign_elementary_condition(statistics, condition):
        parts = condition[1:-1].split()

        var = parts[0].lower()
        relation = parts[1]
        value = float(parts[2])

        clicks = 0
        profit = 0.0
        revenue = 0.0
        cost = 0.0
        leads = 0

        event_2 = 0.0
        event_5 = 0.0

        for offer_stat in statistics:
            clicks += int(offer_stat['clicks'])
            profit += float(offer_stat['profit'])
            revenue += float(offer_stat['revenue'])
            cost += float(offer_stat['cost'])
            leads += int(offer_stat['leads'])
            event_2 += float(offer_stat['event_2'])
            event_5 = float(offer_stat['event_5'])

        if var == 'clicks':
            var = clicks
        elif var == 'profit':
            var = profit
        elif var == 'revenue':
            var = revenue
        elif var == 'cost':
            var = cost
        elif var == 'leads':
            var = leads
        elif var == 'cr':
            if clicks != 0:
                var = (leads / clicks) * 100
            else:
                var = 0
        elif var == 'epc':
            if clicks != 0:
                var = revenue / clicks
            else:
                var = 0
        elif var == 'cpc':
            if clicks != 0:
                var = cost / clicks
            else:
                var = 0
        elif var == 'roi':
            if cost != 0:
                var = profit / cost
            else:
                var = 0
        elif var == 'cpa':
            if leads != 0:
                var = cost / leads
            else:
                var = 0
        elif var == 'approve_%':
            if leads + event_5 != 0:
                var = (event_2 / leads + event_5) * 100
            else:
                var = 0

        if relation == '=':
            return float(var) == value
        elif relation == '<':
            return float(var) < value
        elif relation == '<=':
            return float(var) <= value
        elif relation == '>':
            return float(var) > value
        else:
            return float(var) >= value

    @staticmethod
    def check_campaign_condition(statistics, condition):
        if 'OR' not in condition and 'AND' not in condition:
            return ConditionParser._check_campaign_elementary_condition(statistics, condition)

        condition = condition[1:-1]

        first_cond, conn, second_cond = ConditionParser._split_into_parts(condition)

        if conn == 'AND':
            return ConditionParser.check_campaign_condition(statistics, first_cond) and \
                   ConditionParser.check_campaign_condition(statistics, second_cond)
        else:
            return ConditionParser.check_campaign_condition(statistics, first_cond) or \
                   ConditionParser.check_campaign_condition(statistics, second_cond)

    @staticmethod
    def check_campaign(condition, campaign_id, period, action):
        if not ConditionParser.is_valid(condition):
            return

        campaign = Campaign.objects.get(id__exact=campaign_id)
        if campaign.status == action:
            return False

        campaign_statistics = TrackerManager().get_campaign_info(campaign_id, period)

        return ConditionParser.check_campaign_condition(campaign_statistics, condition)

    @staticmethod
    def is_valid(condition):
        if not ConditionParser.bracket_sequence_is_valid(condition):
            return False

        if not ConditionParser._all_symbols_is_correct(condition):
            return False

        return True
