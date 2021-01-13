# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import re
import time
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.conf import settings

from crontab import CronTab


class Scheduler:
    def __init__(self):
        pass

    @staticmethod
    def _is_time(string):
        try:
            time.strptime(string, '%H:%M')
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_greater(start, end):
        start = time.strptime(start, '%H:%M')
        end = time.strptime(end, '%H:%M')

        return end >= start

    def set_on_crontab(self, schedule, comment, bot_id):
        cron = CronTab(user=settings.CRONTAB_USER)
        command = settings.REDIS_ADDING_COMMAND + f'"{str(bot_id)}"' + 'value'

        weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        cron_day_number = {'sun': 0, 'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6}

        for day in weekdays:
            job = cron.new(command, comment)
            job.day.on(cron_day_number[day])

            if day in schedule:
                for t in schedule[day]:
                    data = t.split(':')

                    job.setall(f'{data[1]} {data[0]} * * {cron_day_number[day]}')

            job.enable()
            cron.write()


    def parse_schedule(self, schedule):
        weekdays = {entry.replace(':', '#', 1).split('#')[0]: entry.replace(':', '#', 1).split('#')[1].strip()
                    for entry in schedule.replace(' ', '').split('\n')}
        weekdays_cleaned = {}

        for weekday in weekdays:
            if not weekdays[weekday]:
                continue

            weekdays_cleaned[weekday] = []
            entries = weekdays[weekday].split(',')

            for entry in entries:
                if '-' not in entry:
                    if self._is_time(entry):
                        weekdays_cleaned[weekday].append(entry)
                    else:
                        raise ValidationError(f"Doesn't look like time: {entry}")
                else:
                    entry = entry.replace('[', '').replace(']', '')
                    re_time_interval = r'^([0-9]{2}:[0-9]{2})-([0-9]{2}:[0-9]{2})([0-9]{1,4})$'
                    if not re.match(re_time_interval, entry):
                        raise ValidationError(f"Doesn't look like time interval: {entry}")

                    data = re.findall(re_time_interval, entry)[0]

                    start, end = data[0], data[1]
                    interval = int(data[2])

                    if interval > 24 * 60:
                        raise ValidationError(f"Checking interval can't be greater than 1440 minutes (24 hours): "
                                              f"{interval}")

                    if not self._is_time(start):
                        raise ValidationError(f"Doesn't look like time: {start}")
                    if not self._is_time(end):
                        raise ValidationError(f"Doesn't look like time: {end}")

                    if not self._is_greater(start, end):
                        raise ValidationError(f"Start point can't be greater than end point: {entry}")

                    if start == end:
                        weekdays_cleaned[weekday].append(start)
                    else:
                        start = datetime.strptime(start, '%H:%M')
                        end = datetime.strptime(end, '%H:%M')

                        while start <= end:
                            weekdays_cleaned[weekday].append(start.strftime('%H:%M'))
                            start += timedelta(minutes=interval)

        return weekdays_cleaned
