import time

from celery import Celery

from server.config import CELERY_BACKEND, CELERY_BROKER

celery = Celery('tasks', broker=CELERY_BROKER, backend=CELERY_BACKEND)


@celery.task(name='tasks.add')
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y
