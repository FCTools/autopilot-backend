"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.conf import settings
from django.db import models


class Campaign(models.Model):
    """
    This model represents campaign from tracker (http://fcttrk.com/?page=Campaigns).
    In addition, there is offers_list - many to many field to Offer model.
    """

    id = models.IntegerField(primary_key=True, verbose_name="ID", unique=True, blank=False, null=False, )

    name = models.CharField(max_length=256, verbose_name="Name", null=True, blank=True, )

    traffic_source = models.ForeignKey(
        "TrafficSource", on_delete=models.CASCADE, verbose_name="Traffic source", blank=False, null=False,
    )

    status = models.SmallIntegerField(verbose_name="Status", null=True, blank=False, default=-1, )

    def __str__(self):
        return f"{self.id} {self.name}"

    def __eq__(self, other):
        if not other:
            return False

        return all(
            [
                self.id == other.id,
                self.name == other.name,
                self.traffic_source == other.traffic_source,
            ]
        )

    def __hash__(self):
        return hash((self.id, self.name, self.traffic_source))
