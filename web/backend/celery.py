"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

import os
import sys

from celery import Celery
from celery.schedules import crontab

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'web')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.backend.settings.dev')

app = Celery('conditions_checker')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'bot_checking': {
        'task': 'bot_manager.tasks.check_bots',
        'schedule': crontab(minute='*/1'),
    },
    'updating': {
        'task': 'bot_manager.tasks.update',
        'schedule': crontab(minute='*/10')
    }
}
