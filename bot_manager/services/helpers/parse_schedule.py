# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import json


def parse_schedule(schedule):
    result = {'mn': [], 'tu': [], 'wd': [], 'th': [], 'fr': [], 'sa': [], 'sn': []}

    for entry in schedule:
        parts = entry.split('-')
        weekday = parts[0]
        time = parts[1].split(':')

        hours = int(time[0])
        minutes = int(time[1])

        result[weekday].append((hours, minutes))

    return json.dumps(result)
