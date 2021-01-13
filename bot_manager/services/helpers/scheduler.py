# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import json
import re
import time

from django.core.exceptions import ValidationError


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

    def parse_schedule(self, schedule):
        weekdays = {entry.replace(':', '#', 1).split('#')[0]: entry.replace(':', '#', 1).split('#')[1].strip()
                    for entry in schedule.replace(' ', '').split('\n')}
        weekdays_cleaned = {}

        for weekday in weekdays:
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
                        raise ValidationError("Checking interval can't be greater than 1440 minutes (24 hours)")

                    if not self._is_time(start):
                        raise ValidationError(f"Doesn't look like time: {start}")
                    if not self._is_time(end):
                        raise ValidationError(f"Doesn't look like time: {end}")

                    if not self._is_greater(start, end):
                        raise ValidationError(f"Start can't be greater than end: {entry}")

                    if start == end:
                        weekdays_cleaned[weekday].append(start)
