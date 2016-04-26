#-*- coding: utf-8 -*-
from __future__ import absolute_import

from .common import *


# Parse database configuration from $DATABASE_URL
import dj_database_url
db_config =  dj_database_url.config()
if db_config:
    DATABASES['default'] =  db_config

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
