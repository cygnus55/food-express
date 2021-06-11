import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodexpress.settings')

# creating an instance of the application
app = Celery('foodexpress')

# doing this, all celery related settings can be added to settings.py file with prefix CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Telling celery to auto discover asynchronous tasks for your applications.
app.autodiscover_tasks()