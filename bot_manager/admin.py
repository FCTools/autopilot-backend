"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.contrib import admin

from bot_manager.models import Bot


@admin.register(Bot)
class AdminBot(admin.ModelAdmin):
    pass
