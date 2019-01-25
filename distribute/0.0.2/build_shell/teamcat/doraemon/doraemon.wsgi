import os
import sys
import django.core.handlers.wsgi
sys.path.append('/web/www/teamcat/doraemon')
os.environ['DJANGO_SETTINGS_MODULE'] = 'doraemon.settings'
application = get_wsgi_application()
