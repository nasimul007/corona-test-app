import ldap
import os

from .licensed import *
from elasticsearch_dsl.connections import connections
import psycopg2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
REPO = os.path.join(BASE_DIR, 'media/repository')

STATIC_ROOT = ''
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
CONVERT_BINARY = '/usr/local/bin/convert'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

SECRET_KEY = ')8d1!=(*5n!o^5^edzzak^^o1klvu69)k_o6vxoet0gh(x0fe('

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'django_template')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'conf.jinja2.environment',
            'extensions': ['jinja2.ext.with_']
        },
    },
]
