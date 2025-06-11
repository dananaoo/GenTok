# backend/tasks.py

from celery_app import celery_app
import time

@celery_app.task
def test_task(name):
    time.sleep(3)
    return f"Hello {name}, task complete!"
