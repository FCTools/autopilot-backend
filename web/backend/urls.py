"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.contrib import admin
from django.urls import path
from bot_manager.views import ListBots, BotCreator, BotDetail, BotStarter, BotStopper, BotDeleter


urlpatterns = [
    path('admin/', admin.site.urls),
    path('bots/list/', ListBots.as_view(), name='bots_list'),
    path('bots/createBot/', BotCreator.as_view(), name='create_bot'),
    path('bots/<int:pk>/', BotDetail.as_view(), name='get_bot'),
    path('bots/startBot/', BotStarter.as_view(), name='start_bot'),
    path('bots/stopBot/', BotStopper.as_view(), name='stop_bot'),
    path('bots/deleteBot/', BotDeleter.as_view(), name='delete_bot'),
]
