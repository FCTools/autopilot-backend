# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from django.contrib import admin
from django.urls import path

from bot_manager.views import log_view, BotCreationView, BotUpdatingView

admin.site.site_header = 'FC Tools Autopilot Administration'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('bots/monitor/', log_view, name='monitor_view'),

    path('bots/createBot/', BotCreationView.as_view(), name='createBot'),
    path('/bots/updateBot/', BotUpdatingView.as_view(), name='updateBot'),
]
