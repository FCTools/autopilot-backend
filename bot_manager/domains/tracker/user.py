"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.db import models


class User(models.Model):
    """
    This model is NOT custom django user.
    This model represents employee from users table in tracker (http://fcttrk.com/?page=Users) with
    some additional parameters (salary group and balances for each traffic group).
    """

    id = models.IntegerField(primary_key=True, verbose_name="ID", null=False, blank=False, unique=True, )

    login = models.CharField(max_length=128, verbose_name="Login", blank=True, null=True, )

    def __str__(self):
        return f"{self.id} {self.login}"

    def __eq__(self, other):
        if not other:
            return False

        return all([self.id == other.id, self.login == other.login])

    def __hash__(self):
        return hash((self.id, self.login))
