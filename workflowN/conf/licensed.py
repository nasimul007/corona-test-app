import datetime

DEBUG = True

ALLOWED_HOSTS = ['*']
APP_HOST = '0.0.0.0:8000'

BRANDING = {
    'BRAND_NAME': 'InfoSapex',
    'PRODUCT_NAME': 'BPMN Process'
}

EXTERNAL_APPS = [
    'rest_framework',
    'oauth2_provider',
    'mptt',
    'debug_toolbar',
    'PyPDF2',
    # 'djcelery_email',
    'django_python3_ldap'
]

CORE_APPS = [
    'apps.core.rbac',
    'apps.core.loginReport',
    'apps.core.announcement',
    'apps.core.todo',
    'apps.core.mail',
    'apps.core.socket_chat',
]

DMS_APPS = [
    'apps.dms.api',
    'apps.dms.api.category',
    'apps.dms.api.document',
    'apps.dms.documents',
    'apps.dms.api.department',
    #'apps.dms.api.branch',
    'apps.dms.api.dms_activity',
]

WORKFLOW_APPS = [
    'apps.workflow.bpmn',
    'apps.workflow.email',
    'apps.workflow.script'
]

INSTALLED_APPS = [
                     'django.contrib.auth',
                     'django.contrib.contenttypes',
                     'django.contrib.sessions',
                     'django.contrib.messages',
                     'django.contrib.staticfiles',
                 ] + EXTERNAL_APPS + CORE_APPS + DMS_APPS + WORKFLOW_APPS

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.core.rbac.ModelBackend.AccountsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'conf.urls'

WSGI_APPLICATION = 'conf.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nrbc',
        'USER': 'nrbc',
        'PASSWORD': 'nrbc@123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_URL = '/login/'

LOGIN_EXEMPT_URLS = (
    r'^api/v1/*',
    r'oauth2_provider/token/',
    r'socket/*',
    r'^workflow/case/account_opening/'
)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# for global authentication
AUTHENTICATION_BACKENDS = ['apps.core.rbac.ModelBackend.EmailOrUsernameModelBackend']

# for ldap authentication
# AUTHENTICATION_BACKENDS += ['django_python3_ldap.auth.LDAPBackend']

AUTH_USER_MODEL = 'rbac.User'

# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#
# SESSION_COOKIE_AGE = 900

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.core.api.authentication.GreenOfficeBasicAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # )
}

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://0.0.0.0/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             # "SOCKET_CONNECT_TIMEOUT": 5,
#             # "SOCKET_TIMEOUT": 5,
#             # "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
#             # "CONNECTION_POOL_KWARGS": {"max_connections": 100},
#         }
#     }
# }

# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "default"

# INTERNAL_IPS = ('127.0.0.1',)

# Elastic Search config
ELASTIC_HOST = 'localhost'
ELASTIC_PORT = 9200
WORKFLOW_SEARCH_INDICES = 'raw-workflow'
DMS_SEARCH_INDICES = 'raw-dms'

# Application config
DMS = "9dL53eBFDK"
# DMS = ""
#WORKFLOW = "aBX3RODumf"
WORKFLOW = ""

# change if deploy only DMS or Workflow
PRODUCT_NAME = 'DigiFlow'


# user level config
#USER_DMS = "1q2w3e"
# USER_DMS = ""
#USER_WORKFLOW = "1q2w3e"
#USER_WORKFLOW = ""

# Mail config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'infosapex2@gmail.com'
EMAIL_HOST_PASSWORD = 'info123456'
EMAIL_USE_TLS = True

EMAIL_SEND_LIMIT_AT_ONE_BATCH = 50
EMAIL_SEND_ATTEMPT_TIMES = 3
EFORM_VARIABLE_APPEAR_IN_EMAIL = [{'variable': 'name', 'label': 'Name'}, {'variable': 'country', 'label': 'Country'}]

CELERY_EMAIL_TASK_CONFIG = {
    'name': 'djcelery_email_send',
    'ignore_result': False,
}

# Workflow Config
RISK_TASK_PERCENTAGE = 60

# Client Code
# CLIENT_NAME = 'xcb59hj'
# CLIENT_NAME = 'e78tfb9'
#CLIENT_NAME = 'z8t5y67'     # Apollo
# CLIENT_NAME = 'aw6io2a' #Ebl
CLIENT_NAME = 'NRBC'
# will be appear under mail
CLIENT_COMPANY_NAME = 'Infosapex Limited'

# open task with out login settings
CAN_OPEN_TASK_WITHOUT_LOGIN = False
OUT_TASK_ID = 10
OUT_USER = 'rawnak'
OUT_PASSWORD = 'admin'


# mail notification for document expiry
DAYS = 2

# CELERY SETTINGS
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

SESSION_COOKIE_AGE = 1800
SESSION_SAVE_EVERY_REQUEST = True

SOCKET_LISTENING_PORT = 4000

# Log config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s::(%(process)d %(thread)d)::%(module)s - %(message)s'
        },
    },
    'handlers': {
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'log/critical_error-{}.log'.format(datetime.datetime.now().date()),
            'formatter': 'default'
        },
        'warning': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'log/error-{}.log'.format(datetime.datetime.now().date()),
            'formatter': 'default'
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    'loggers': {
        'django': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': False,
        },
        'warning_logger': {
            'handlers': ['warning'],
            'level': 'WARNING',
            'propagate': False,
        },
        "django_python3_ldap": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },

}

# The URL of the LDAP server.
LDAP_AUTH_URL = "ldap://localhost"
LDAP_AUTH_USE_TLS = False
LDAP_AUTH_SEARCH_BASE = 'dc=infosapex,dc=com'
LDAP_AUTH_OBJECT_CLASS = 'inetOrgPerson'

LDAP_AUTH_USER_LOOKUP_FIELDS = ('username',)
LDAP_AUTH_CLEAN_USER_DATA = 'django_python3_ldap.utils.clean_user_data'
LDAP_AUTH_SYNC_USER_RELATIONS = 'django_python3_ldap.utils.sync_user_relations'
LDAP_AUTH_FORMAT_SEARCH_FILTERS = 'django_python3_ldap.utils.format_search_filters'
# LDAP_AUTH_FORMAT_USERNAME = 'django_python3_ldap.utils.format_username_active_directory'
# LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = 'infosapex.com'
# LDAP_AUTH_CONNECTION_USERNAME = 'cn=admin,dc=infosapex,dc=com'
# LDAP_AUTH_CONNECTION_PASSWORD = '123456'

LDAP_AUTH_USER_FIELDS = {
    "username": "uid",
    "email": "mail"
}
