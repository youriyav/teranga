"""
WSGI config for senfood project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
sys.path.append("/home/teranga")
os.environ["DJANGO_SETTINGS_MODULE"]="senfood.settings"

application = get_wsgi_application()
