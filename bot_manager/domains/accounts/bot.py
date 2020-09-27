"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.db import models


class Bot(models.Model):
    name = models.CharField(verbose_name="Name", max_length=128, null=False, blank=False, )

    """
    There are 2 types of bots: 
    first type (1) - these bots check landings for each campaign and add these landings to black/white list
    second type (2) - these bots check campaigns and stop/start it depending on condition
    """
    type = models.PositiveSmallIntegerField(verbose_name="Type", null=False, blank=False, choices=((1, 1), (2, 2)))

    user = models.ForeignKey(to="User", verbose_name="User", null=False, blank=False, on_delete=models.CASCADE, )

    campaigns_list = models.ManyToManyField(to="Campaign", verbose_name="Campaigns list", )

    condition = models.TextField(max_length=16384, verbose_name="Condition", null=False, blank=False, )

    action = models.CharField(max_length=128, verbose_name="Action", null=False, blank=False,
                              choices=(("stop_campaign", "Stop campaign"),
                                       ("start_campaign", "Start campaign"),
                                       ("add_to_bl", "Add landing to BL"),
                                       ("add_to_wl", "Add landing to WL"), ))

    checking_interval = models.PositiveIntegerField(verbose_name="Condition checking interval", )

    # following 2 fields are only for bots type 1

    # list_type can be only 0 - white list, and 1 - black_list
    list_type = models.PositiveSmallIntegerField(verbose_name="List type", null=True, blank=False, default=None, )

    landing_exceptions = models.TextField(verbose_name="Landing exceptions", null=True, blank=True, default=None, )

