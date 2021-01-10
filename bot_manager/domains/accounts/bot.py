# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from django.db import models


class Bot(models.Model):
    name = models.CharField(verbose_name="Name", max_length=128, null=False, blank=False, )

    """
    There are 2 types of bots: 
    first type (1) - these bots check landings for each campaign and add these landings to black/white list
    second type (2) - these bots check campaigns and stop/start it depending on condition
    """
    type = models.PositiveSmallIntegerField(verbose_name="Type", null=False, blank=False, choices=((1, 1), (2, 2)))

    user = models.IntegerField(verbose_name="User", null=False, blank=False, )

    traffic_source = models.CharField(verbose_name="Traffic source", max_length=256, null=False, blank=False,
                                      choices=(("Propeller Ads", "Propeller Ads"),))

    campaigns_list = models.ManyToManyField(to="Campaign", verbose_name="Campaigns list", )

    condition = models.TextField(max_length=16384, verbose_name="Condition", null=False, blank=False, )

    status = models.CharField(verbose_name="Status (enabled/disabled)", max_length=8, null=False, blank=False,
                              default="enabled", choices=(("enabled", "enabled"), ("disabled", "disabled")))

    action = models.SmallIntegerField(verbose_name="Action", null=False, blank=False,
                                      choices=((2, "Stop campaign"),
                                               (1, "Start campaign"),))

    schedule = models.TextField(verbose_name="Schedule", max_length=65536, null=False, blank=False, default="-", )

    period = models.PositiveIntegerField(verbose_name="Period for statistics checking", null=False, blank=False, )

    ignored_sources = models.TextField(verbose_name="Ignored sources", null=True, blank=False, default=None, )

    source_info = models.TextField(verbose_name="Source info", max_length=65536, null=True, blank=False, default=None, )

    def __str__(self):
        return f'{self.id} {self.name} {self.status}'
