import os
import sys

sys.path.append('/var/www/nihlapp')

os.environ['PYTHON_EGG_CACHE'] = '/tmp/nihlapp/python-eggs'
os.environ['DJANGO_SETTINGS_MODULE'] = 'nihlapp.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
