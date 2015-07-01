"""
Django settings for tests project.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'django-basic-models-behaviors-secret-key'

INSTALLED_APPS = (
    'tests',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
