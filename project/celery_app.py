import os
import time
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app =Celery('project')
# IMPORTANT! mention namespace
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf_broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task()
def debug_task():
    time.sleep(5)
    print('from debug task')