# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from django import forms


class LogFilterForm(forms.Form):

    log_type = forms.ChoiceField(
        choices=[('actions-log', 'actions-log'),
                 ('environment-log', 'environment-log'),
                 ('server-load', 'server-load'),
                 ('ts-log', 'ts-log'), ],
        initial='actions-log',
        widget=forms.Select,
    )

    bot_id = forms.IntegerField(required=False)

    def clean(self):
        return self.cleaned_data
