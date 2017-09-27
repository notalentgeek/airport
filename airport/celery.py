""" Basic setup for Celery. """

from celery import Celery
from django.conf import settings
import os

"""
Indicate Celery to use the default Django settings module.

CAUTION: Make sure the application name is the same listed in settings.py.
Otherwise Gunicorn cannot be ran.
"""
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airport.settings")

""" Initial setup. """
app = Celery("airport")
app.config_from_object("django.conf:settings")

"""
This codes below will tell Celery to autodiscover all your tasks.py that are
in your application folders.
"""
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)