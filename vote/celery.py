import os
import time

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VoteProject.settings')

app = Celery('VoteProject')

app.config_from_object('django.conf:settings')


app.autodiscover_tasks()

@app.task()
def debug_task():
    time.sleep(20)


app.conf.beat_schedule = {
    'add-every-60-seconds': {
        'task': 'vote.tasks.migrate_votes',
        'schedule': 3600.0,
    },
}
