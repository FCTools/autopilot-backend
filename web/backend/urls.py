"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.contrib import admin
from django.urls import path
from bot_manager.views import ListBots, BotCreator


urlpatterns = [
    path('admin/', admin.site.urls),
    path('bots/list/', ListBots.as_view(), name='getBots'),
    path('bots/createBot/', BotCreator.as_view(), name='createBot'),
]
