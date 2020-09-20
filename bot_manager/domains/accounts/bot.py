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
    type = models.PositiveSmallIntegerField(verbose_name="Type", null=False, blank=False, choices=(1, 2))

    campaigns_list = models.ManyToManyField(to="Campaign", verbose_name="Campaigns list", null=False, blank=False, )

    condition = models.TextField(max_length=16384, verbose_name="Condition", null=False, blank=False, )

    action = models.CharField(max_length=128, verbose_name="Action", null=False, blank=False,
                              choices=("Stop campaign, Start campaign", "Add landing to BL", "Add landing to WL"), )

    checking_interval = models.TimeField(verbose_name="Condition checking interval", )

    # following 2 fields are only for bots type 1
    list_type = models.PositiveSmallIntegerField(verbose_name="List type", null=True, blank=False, )

    landing_exceptions = models.TextField(verbose_name="Landing exceptions", null=True, blank=True, )

