# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from django.db import models


class Site(models.Model):
    """
    This model represents site (source/zone).
    """

    site_id = models.CharField(verbose_name="Site ID", max_length=2048, null=False, blank=False, )

    campaign = models.ForeignKey(to="Campaign", verbose_name="Campaign ID", null=False, blank=False,
                                    on_delete=models.CASCADE, )

    name = models.CharField(verbose_name="Name", max_length=2048, null=True, blank=False, )

    status = models.SmallIntegerField(verbose_name="Status (added to wl/bl)", null=False, blank=False, )

    def __str__(self):
        return f'{self.site_id}'

