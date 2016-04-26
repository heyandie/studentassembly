"""
WSGI config for studentassembly project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studentassembly.settings.development")

from whitenoise.django import DjangoWhiteNoise
from django.core.wsgi import get_wsgi_application
from dj_static import Cling
import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

if os.environ.get('DJANGO_SETTINGS_MODULE', None) == 'studentassembly.settings.staging':
    application = Cling(get_wsgi_application())
    application = DjangoWhiteNoise(application)
