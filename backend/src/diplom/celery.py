# diplom/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplom.settings')


app = Celery('diplom')
app.config_from_object('django.conf:settings', namespace='CELERY')

print(app.conf.broker_url)
app.autodiscover_tasks(['pravo', 'diplom'])
