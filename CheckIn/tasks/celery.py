# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
#
# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
#
# # create a Celery instance and configure it using the settings from Django
# app = Celery('project')
#
# # Load task modules from all registered Django app configs.
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Auto-discover tasks in all installed apps
# app.autodiscover_tasks()
#
#
from celery import Celery
from django.conf import settings

app = Celery('your_project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

