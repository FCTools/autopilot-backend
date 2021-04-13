# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import logging
from string import ascii_letters, digits

from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string

from bot_manager.services.helpers.scheduler import Scheduler

_logger = logging.getLogger(__name__)


class Bot(models.Model):
    name = models.CharField(verbose_name="Name", max_length=128, null=False, blank=False,
                            help_text="Any string up to 128 characters", )

    """
    You can read about bot types in documentation (can be found in YouTrack).
    """
    type = models.PositiveSmallIntegerField(verbose_name="Type", null=False, blank=False,
                                            choices=((settings.PLAY_STOP_CAMPAIGN, "Play/stop campaign"),
                                                     (settings.INCLUDE_EXCLUDE_ZONE, "Add to black/white list"),), )

    user = models.IntegerField(verbose_name="User", null=False, blank=False,
                               help_text="Only superuser can change this field", )

    traffic_source = models.ForeignKey(verbose_name="Traffic source", to='TrafficSource', null=False, blank=False,
                                       on_delete=models.DO_NOTHING, )

    tracker = models.CharField(verbose_name="Tracker", null=False, blank=False, max_length=64, )

    tracker_api_key = models.CharField(verbose_name="Tracker API key", max_length=128, null=False, blank=False, )

    tracker_url = models.CharField(verbose_name="Tracker url for requests", max_length=256, null=False, blank=False, )

    campaigns_list = models.JSONField(verbose_name="Campaigns",
                                      help_text="If campaign doesn't exist, you can create it here using \"+\".")

    condition = models.TextField(max_length=16384, verbose_name="Condition", null=False, blank=False,
                                 help_text="Example: ((CR < 1) & (clicks >= 50))", )

    status = models.CharField(verbose_name="Status (enabled/disabled)", max_length=8, null=False, blank=False,
                              default=settings.ENABLED,
                              choices=((settings.ENABLED, settings.ENABLED), (settings.DISABLED, settings.DISABLED)), )

    action = models.SmallIntegerField(verbose_name="Target action", null=False, blank=False,
                                      choices=((settings.STOP_CAMPAIGN, "Stop campaign"),
                                               (settings.PLAY_CAMPAIGN, "Play campaign"),
                                               (settings.EXCLUDE_ZONE, "Exclude zone"),
                                               (settings.INCLUDE_ZONE, "Include zone"),))

    ts_api_key = models.CharField(verbose_name="TS api key", max_length=128, null=False, blank=False, )

    schedule = models.TextField(verbose_name="Schedule", max_length=16384, null=False, blank=False,
                                default="mon: \ntue: \nwed: \nthu: \nfri: \nsat: \nsun: \n",
                                help_text="Example: mon: 10:00-12:30[5], 13:30, 15:00-18:00[10]. "
                                          "Note that checking interval can't be greater than 1440 minutes "
                                          "(24 hours). All time is UTC time.", )

    period = models.SmallIntegerField(verbose_name="Period for statistics checking", null=False, blank=False,
                                      choices=((settings.TODAY, "Today"),
                                               (settings.YESTERDAY, "Yesterday"),
                                               (settings.THIS_WEEK, "This week"),
                                               (settings.LAST_2_DAYS, "Last 2 Days"),
                                               (settings.LAST_3_DAYS, "Last 3 Days"),
                                               (settings.LAST_7_DAYS, "Last 7 Days"),
                                               (settings.LAST_14_DAYS, "Last 14 Days"),
                                               (settings.THIS_MONTH, "This month"),
                                               (settings.LAST_MONTH, "Last month"),
                                               (settings.THIS_YEAR, "This year"),
                                               (settings.ALL_TIME, "All time"),
                                               ),
                                      )

    list_to_add = models.CharField(max_length=128, verbose_name="List (audience for evadav)", null=True, blank=True,
                                   default="-", )

    crontab_comment = models.CharField(max_length=256, verbose_name="Crontab task comment", null=False, blank=False,
                                       default="empty", )

    ignored_zones = models.TextField(verbose_name="Ignored zones", null=True, blank=True, default=None,
                                     help_text="Please specify each zone on a new line", )

    client_id = models.CharField(max_length=128, verbose_name="Client key (for mgid)", null=True, blank=True,
                                 default="-", )

    def delete(self, *args, **kwargs):
        Scheduler().clear_jobs(self.crontab_comment)
        super(Bot, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        _logger.info("Start bot saving")
        self.condition = self.condition.replace('AND', '&').replace('OR', '|')

        scheduler = Scheduler()
        prev_status = None

        if self.pk:
            _logger.info("Already existing bot. Checking schedule...")

            this_bot_db = Bot.objects.get(pk=self.pk)
            prev_schedule = this_bot_db.schedule
            prev_status = this_bot_db.status

            if self.schedule != prev_schedule:
                scheduler.clear_jobs(this_bot_db.crontab_comment)
                self.crontab_comment = "empty"

                _logger.info("Schedule changing detected. Clear old schedule and set crontab comment to default.")

        if self.crontab_comment == "empty":
            _logger.info("Generate new crontab-comment...")
            salt = get_random_string(16, ascii_letters + digits)
            self.crontab_comment = str(hash(salt))

            parsed_schedule = scheduler.parse_schedule(self.schedule)
            super(Bot, self).save(*args, **kwargs)
            _logger.info("Call super-save.")

            if parsed_schedule:
                scheduler.set_on_crontab(parsed_schedule, self.crontab_comment, self.id)
            _logger.info("Set new schedule to crontab.")

            if self.status == settings.DISABLED:
                scheduler.disable_jobs(self.crontab_comment)

            return

        else:
            super(Bot, self).save(*args, **kwargs)

        if prev_status and prev_status != self.status:
            if self.status == settings.DISABLED:
                scheduler.disable_jobs(self.crontab_comment)
            else:
                scheduler.enable_jobs(self.crontab_comment)

        _logger.info(f"Bot was successfully saved: {self.name}")

    def __str__(self):
        return f'{self.pk} {self.name} {self.status}'
