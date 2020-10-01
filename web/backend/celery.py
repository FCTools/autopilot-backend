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
    'monday-statistics-email': {
       'task': 'bot_manager.tasks.print_hello',
       'schedule': crontab(minute='*/1'),
   }
}
