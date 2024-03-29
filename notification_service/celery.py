import os

from celery import Celery, shared_task


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notification_service.settings")

app = Celery("notification_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["api.tasks"])
