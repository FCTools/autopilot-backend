# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string

from bot_manager.services.helpers.scheduler import Scheduler


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
                                help_text="Example: mon: 10:00-12:30[5], 13:30, 15:00-18:00[10]. "
                                          "Note that checking interval can't be greater than 1440 minutes "
                                          "(24 hours).", )

    period = models.PositiveIntegerField(verbose_name="Period for statistics checking", null=False, blank=False,
                                         help_text="Please specify the value in seconds", )

    crontab_comment = models.CharField(max_length=256, verbose_name="Crontab task comment", null=False, blank=False,
                                       default="empty",)

    ignored_sources = models.TextField(verbose_name="Ignored sources", null=True, blank=False, default=None, )

    # BUG: bot jobs doesn't clear
    def delete(self, *args, **kwargs):
        Scheduler().clear_jobs(self.crontab_comment)
        super(Bot, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        scheduler = Scheduler()
        prev_status = None

        if self.id:
            this_bot_db = Bot.objects.get(pk=self.id)
            prev_schedule = this_bot_db.schedule
            prev_status = this_bot_db.status

            if self.schedule != prev_schedule:
                scheduler.clear_jobs(this_bot_db.crontab_comment)
                self.crontab_comment = "empty"

        if self.crontab_comment == "empty":
            salt = get_random_string(16, 'qwertyuiopasdfghjklzxcvbnm0123456789')
            self.crontab_comment = str(hash(salt))

            parsed_schedule = scheduler.parse_schedule(self.schedule)
            super(Bot, self).save(*args, **kwargs)

            scheduler.set_on_crontab(parsed_schedule, self.crontab_comment, self.id)

            if self.status == "disabled":
                scheduler.disable_jobs(self.crontab_comment)

            return

        else:
            super(Bot, self).save(*args, **kwargs)

        if prev_status and prev_status != self.status:
            if self.status == "disabled":
                scheduler.disable_jobs(self.crontab_comment)
            else:
                scheduler.enable_jobs(self.crontab_comment)

    def __str__(self):
        return f'{self.id} {self.name} {self.status}'
