import os
from celery import Celery
from pathlib import Path
import sys
from datetime import timedelta
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

app = Celery('django_celery')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spiderManage.settings')

app.config_from_object('task_celery.config')

app.autodiscover_tasks([
    'task_celery.node_status'
])

app.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'task_celery.node_status.tasks.node_detection',
        # 每6秒执行一次
        'schedule': 12,
        # 每年4月11如8点42分执行
        # 'schedule':crontab(minute=42, hour=8, day_of_month=11, month_of_year=4)
        # 'args': ('云海',)
    }
}
# 定时 celery -A task_celery.main beat -l info
# 消费 celery -A task_celery.main worker --loglevel=info -P eventlet
