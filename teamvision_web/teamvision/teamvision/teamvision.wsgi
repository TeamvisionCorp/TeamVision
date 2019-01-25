import os
import sys
import django.core.handlers.wsgi
sys.path.append('/web/www/teamvision/teamvision')
os.environ['DJANGO_SETTINGS_MODULE'] = 'teamvision.settings'
application = get_wsgi_application()
