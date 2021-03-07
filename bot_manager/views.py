# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from bot_manager.forms import LogFilterForm


@login_required(login_url='/admin/login/')
def log_view(request):
    template = 'statistics_page.html'

    if request.method == "POST":
        form = LogFilterForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['log_type'] == 'environment-log':
                env_log_path = os.getenv('ENV_LOG_PATH')
                if not env_log_path:
                    return render(request, template)

                with open(env_log_path, 'r', encoding='utf-8') as file:
                    log = file.read().split('\n')

                return render(request, template, context={'log': list(reversed(log)), 'form': form,
                                                          'log_type': 'environment log'})

            bot_id = form.cleaned_data["bot_id"]

            autopilot_engine_log_path = os.getenv("ACTIONS_LOG_PATH")
            if not autopilot_engine_log_path:
                return render(request, template)

            pattern = f'Bot id: {bot_id}'

            with open(autopilot_engine_log_path, 'r', encoding='utf-8') as file:
                log = file.read().split('\n')

            if not bot_id:
                return render(request, template, context={'bot_id': bot_id, 'log': list(reversed(log)),
                                                          'form': form, 'log_type': 'actions log'})

            result = [line for line in log if pattern in line]

            return render(request, template, context={'bot_id': bot_id, 'log': list(reversed(result)),
                                                      'form': form, 'log_type': 'actions log'})
        else:
            return render(request, template, {'form': form})

    else:
        form = LogFilterForm()
        return render(request, template, {"form": form})
