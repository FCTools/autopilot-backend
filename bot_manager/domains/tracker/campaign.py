"""
Copyright © 2020-2021 FC Tools.
All rights reserved.
Author: German Yakimov
"""

from django.db import models


class Campaign(models.Model):

    # id from traffic source
    id = models.IntegerField(primary_key=True, verbose_name="ID", unique=True, blank=False, null=False, )

    name = models.CharField(max_length=256, verbose_name="Name", null=True, blank=True, )

    traffic_source = models.CharField(verbose_name="Traffic source", blank=False, null=False,
                                      choices=(("Propeller Ads", "Propeller Ads"),),
                                      max_length=256, )

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
