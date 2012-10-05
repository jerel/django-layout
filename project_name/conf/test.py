from {{ project_name }}.settings import *   # pylint: disable=W0614,W0401

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# or use postgres if this is what we're deploying to.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': '{{ project_name }}',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#     }
# }

INSTALLED_APPS += (
    'django.contrib.admin'
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# speeds up the tests
PASSWORD_HASHERS = ('django.contrib.auth.hashers.CryptPasswordHasher', )
