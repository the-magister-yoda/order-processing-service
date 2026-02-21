import os
from celery import Celery

broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")

celery_app = Celery(
    "order_service",
    broker=broker_url,
    backend=broker_url,
)

# ВАЖНО — автопоиск задач
celery_app.autodiscover_tasks(["app.tasks"])

# ВАЖНО — принудительный импорт
import app.tasks.order_tasks
