import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'residential_parking_permit.settings')

app = Celery('residential_parking_permit')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
