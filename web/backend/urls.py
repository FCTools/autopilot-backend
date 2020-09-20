"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
