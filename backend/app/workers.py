from celery import Celery
import os

celery_app = Celery(
    "workers",
    broker=os.getenv("REDIS_URL", "redis://redis:6379"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379")
)