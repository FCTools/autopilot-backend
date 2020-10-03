"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

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
