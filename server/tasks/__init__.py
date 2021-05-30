import time

from celery import Celery

from server.config import Config

celery = Celery('tasks', broker=Config.CELERY_BROKER, backend=Config.CELERY_BACKEND)


@celery.task(name='tasks.add')
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y
