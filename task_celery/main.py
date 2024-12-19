import os
import sys
from datetime import timedelta
from pathlib import Path

import django
from celery import Celery

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

app = Celery('django_celery')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crawlsy.settings')

django.setup()
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks([
    'task_celery.node_status',
    'task_celery.task_start'
])

app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
# app.conf.beat_schedule = {
#     'node-heartbeat-12-seconds': {
#         'task': 'task_celery.node_status.tasks.node_detection',
#         'schedule': timedelta(seconds=12),
#     }
# }
# 定时 celery -A task_celery.main beat -l info
# 消费 celery -A task_celery.main worker --loglevel=info -P eventlet
