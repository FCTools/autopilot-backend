"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.contrib import admin

from bot_manager.models import Bot, TrafficSource, Campaign, Site


@admin.register(Bot)
class AdminBot(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'user', 'condition', 'status', 'action']


@admin.register(TrafficSource)
class AdminTrafficSource(admin.ModelAdmin):
    list_display = ['id', 'name', 'filtering_param_name_sources', 'filtering_param_name_campaigns']


@admin.register(Campaign)
class AdminCampaign(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']


@admin.register(Site)
class AdminSite(admin.ModelAdmin):
    list_display = ['site_id', 'campaign', 'name', 'status']
