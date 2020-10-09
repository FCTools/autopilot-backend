"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.contrib import admin

from bot_manager.models import Bot, User, TrafficSource, Campaign, Offer, Site


@admin.register(Bot)
class AdminBot(admin.ModelAdmin):
    pass


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    pass


@admin.register(Offer)
class AdminOffer(admin.ModelAdmin):
    pass


@admin.register(TrafficSource)
class AdminTrafficSource(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'filtering_param_name']


@admin.register(Campaign)
class AdminCampaign(admin.ModelAdmin):
    pass


@admin.register(Site)
class AdminSite(admin.ModelAdmin):
    pass
