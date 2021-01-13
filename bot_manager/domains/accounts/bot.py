# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from django.db import models
from django.conf import settings


class Bot(models.Model):
    name = models.CharField(verbose_name="Name", max_length=128, null=False, blank=False, )

    """
    There are 2 types of bots: 
    second type (2) - these bots check landings for each campaign and add these landings to black/white list
    first type (1) - these bots check campaigns and stop/start it depending on condition
    """
    type = models.PositiveSmallIntegerField(verbose_name="Type", null=False, blank=False,
                                            choices=((1, "Play/stop campaign"),),)

    user = models.ForeignKey(verbose_name="User", null=True, blank=False, to=settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, )

    traffic_source = models.CharField(verbose_name="Traffic source", max_length=256, null=False, blank=False,
                                      choices=(("Propeller Ads", "Propeller Ads"),))

    campaigns_list = models.ManyToManyField(to="Campaign", verbose_name="Campaigns list",
                                            help_text="If campaign doesn't exist, you can create it using \"+\"")

    condition = models.TextField(max_length=16384, verbose_name="Condition", null=False, blank=False,
                                 help_text="Example: ((CR < 1) & (clicks >= 50))", )

    status = models.CharField(verbose_name="Status (enabled/disabled)", max_length=8, null=False, blank=False,
                              default="enabled", choices=(("enabled", "enabled"), ("disabled", "disabled")), )

    action = models.SmallIntegerField(verbose_name="Target action", null=False, blank=False,
                                      choices=((2, "Stop campaign"),
                                               (1, "Start campaign"),))

    ts_api_key = models.CharField(verbose_name="TS api key", max_length=1024, null=False, blank=False,)

    schedule = models.TextField(verbose_name="Schedule", max_length=65536, null=False, blank=False,
                                default="mon: \ntue: \nwed: \nthu: \nfri: \nsat: \nsun: \n",
                                help_text="Example: mon: 10:00-12:30[5], 13:30, 15:00-18:00[10]", )

    period = models.PositiveIntegerField(verbose_name="Period for statistics checking", null=False, blank=False,
                                         help_text="Please specify the value in seconds")

    ignored_sources = models.TextField(verbose_name="Ignored sources", null=True, blank=False, default=None, )

    def __str__(self):
        return f'{self.id} {self.name} {self.status}'
