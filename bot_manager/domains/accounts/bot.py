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

    status = models.CharField(verbose_name="Status (enabled/disabled)", max_length=8, null=False, blank=False,
                              default="disabled", choices=(("enabled", "enabled"), ("disabled", "disabled")))

    action = models.SmallIntegerField(verbose_name="Action", null=False, blank=False,
                                      choices=((3, "Stop campaign"),
                                               (4, "Start campaign"),
                                               (2, "Add landing to BL"),
                                               (1, "Add landing to WL"),))

    schedule = models.TextField(verbose_name="Schedule", max_length=65536, null=False, blank=False, default="-", )

    period = models.PositiveIntegerField(verbose_name="Period for statistics checking", null=False, blank=False, )

    ignored_sources = models.TextField(verbose_name="Ignored sources", null=True, blank=False, default=None, )
