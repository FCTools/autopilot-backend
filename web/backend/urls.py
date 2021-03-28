# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from django.contrib import admin
from django.urls import path

from bot_manager.views import (log_view,
                               BotCreationView,
                               BotUpdatingView,
                               BotInfoView,
                               BotListView,
                               BotDeletingView,
                               BotStartingView,
                               BotStoppingView)

admin.site.site_header = 'FC Tools Autopilot Administration'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('bots/monitor/', log_view, name='monitor'),

    path('bots/createBot/', BotCreationView.as_view(), name='createBot'),
    path('/bots/updateBot/', BotUpdatingView.as_view(), name='updateBot'),
    path('/bots/stopBot/', BotStoppingView.as_view(), name='stopBot'),
    path('/bots/startBot/', BotStartingView.as_view(), name='startBot'),
    path('/bots/deleteBot/', BotDeletingView.as_view(), name='deleteBot'),
    path('/bots/getList/', BotListView.as_view(), name='getList'),
    path('/bots/getBot/', BotInfoView.as_view(), name='getBot'),
]
