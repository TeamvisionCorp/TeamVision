#coding=utf-8
# entry point for the Django loop

import os 

os.environ.update(DJANGO_SETTINGS_MODULE='doraemon.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
