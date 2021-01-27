# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from django.db import models


class TrafficSource(models.Model):
    name = models.CharField(max_length=256, verbose_name="Traffic source", null=False, blank=False, unique=True, )

    # param for filtering campaign statistics by zones
    filter_param_number = models.SmallIntegerField(verbose_name="Param number in tracker", null=False, blank=False, )

    def __str__(self):
        return self.name
