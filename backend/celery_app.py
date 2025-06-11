# celery_app.py
from celery import Celery
from dotenv import load_dotenv
load_dotenv()
app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

app.conf.task_routes = {
    "tasks.*": {"queue": "default"},
}
