# Django settings for tests project.

import os.path

PROJECT_ROOT = os.path.dirname(__file__)

INSTALLED_APPS = (
    'basic_models_behaviors',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'tests.db'),
    }
}

SECRET_KEY = 'django-basic-models-behaviors-secret-key'
INTERNAL_IPS = ('127.0.0.1')
