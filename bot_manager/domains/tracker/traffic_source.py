"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.db import models


class TrafficSource(models.Model):
    """
    This model represents traffic source from corresponding table from tracker
    (http://fcttrk.com/?page=Traffic_Sources).
    """

    id = models.IntegerField(primary_key=True, verbose_name="ID", null=False, blank=False, unique=True, )

    name = models.CharField(max_length=128, verbose_name="Name", null=True, blank=True, )

    filtering_param_name = models.CharField(verbose_name="Param name for filtering campaign's statistics by sources.",
                                            max_length=256, null=True, blank=False, default=None, )

    filtering_param_number = models.PositiveSmallIntegerField(
        verbose_name="Number of param for filtering campaign's statistics by sources.", null=True, blank=False,
        default=None, )

    def __str__(self):
        return f"{self.id} {self.name}"

    def __eq__(self, other):
        if not other:
            return False

        return all([self.id == other.id, self.name == other.name])

    def __hash__(self):
        return hash((self.id, self.name))
