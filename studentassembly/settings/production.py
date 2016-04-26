#-*- coding: utf-8 -*-
from __future__ import absolute_import

from .common import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'studentassembly',
        'USER' : 'studentassembly',
        'PASSWORD' : 'corruptionsucks',
        'HOST' : 'studentassembly.creqomyfyjoe.us-west-2.rds.amazonaws.com',
        'PORT' : '5432',
    }
}


INSTALLED_APPS += ('storages',)
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL
