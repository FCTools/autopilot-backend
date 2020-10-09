"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.db import models


class Site(models.Model):
    """
    This model represents site (source/zone).
    """

    site_id = models.CharField(verbose_name="Site ID", max_length=512, null=False, blank=False, )

    campaign = models.ForeignKey(to="Campaign", verbose_name="Campaign ID", null=False, blank=False,
                                    on_delete=models.CASCADE, )

    name = models.CharField(verbose_name="Name", max_length=512, null=True, blank=False, )

    status = models.SmallIntegerField(verbose_name="Status (added to wl/bl)", null=False, blank=False, )

