# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

from django.contrib import admin
from django.urls import path

from bot_manager.views import BotCreator, BotStarter, BotStopper, BotDeleter, BotUpdater

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bots/createBot/', BotCreator.as_view(), name='create_bot'),
    path('bots/startBot/', BotStarter.as_view(), name='start_bot'),
    path('bots/stopBot/', BotStopper.as_view(), name='stop_bot'),
    path('bots/deleteBot/', BotDeleter.as_view(), name='delete_bot'),
    path('bots/editBot/', BotUpdater.as_view(), name='edit_bot'),
]
