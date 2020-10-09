"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.contrib import admin

from bot_manager.models import Bot, User, TrafficSource, Campaign, Offer, Site


@admin.register(Bot)
class AdminBot(admin.ModelAdmin):
    list_display = ['name', 'type', 'user', 'condition', 'status', 'action']


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['id', 'login']


@admin.register(Offer)
class AdminOffer(admin.ModelAdmin):
    list_display = ['id', 'name', 'network']


@admin.register(TrafficSource)
class AdminTrafficSource(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'filtering_param_name']


@admin.register(Campaign)
class AdminCampaign(admin.ModelAdmin):
    list_display = ['id', 'name', 'traffic_group', 'status', 'user']


@admin.register(Site)
class AdminSite(admin.ModelAdmin):
    list_display = ['site_id', 'campaign', 'name', 'status']
