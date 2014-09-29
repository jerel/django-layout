"""
Local test settings
"""
from {{ project_name }}.settings.test import *   # pylint: disable=W0614,W0401


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': '{{ project_name }}',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '',
#     }
# }
