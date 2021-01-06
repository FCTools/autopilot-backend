"""
Copyright © 2020-2021 FC Tools.
All rights reserved.
Author: German Yakimov
"""

from django.contrib import admin

from bot_manager.models import Bot, Campaign, Site


@admin.register(Bot)
class AdminBot(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'user', 'condition', 'status', 'action']


@admin.register(Campaign)
class AdminCampaign(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Site)
class AdminSite(admin.ModelAdmin):
    list_display = ['site_id', 'campaign', 'name', 'status']
