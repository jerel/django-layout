from {{ project_name }}.settings import *   # pylint: disable=W0614,W0401

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('You', 'your@email'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ project_name }}',
        'USER': '{{ project_name }}',
        'PASSWORD': '{{ project_name }}',
        'HOST': '127.0.0.1',
    }
}

ROOT_URLCONF = '{{ project_name }}.settings.local.urls'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

