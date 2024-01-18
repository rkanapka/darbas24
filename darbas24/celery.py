from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "darbas24.settings")
app = Celery("darbas24")
app.conf.timezone = "UTC"
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.autodiscover_tasks(["scraper"], related_name="sites.cvbankas")
