from decouple import config
from .base import *


DEBUG = False

ADMINS = [
    ('jonadmin don', 'prodenv001@gmail.com')
]

ALLOWED_HOSTS = ['educaproject.com', 'www.educaproject.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

REDIS_URL = 'redis://redis:6379/1'
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [REDIS_URL]
# CACHES['default']['LOCATION'] = REDIS_URL
# already set up in settings/base.py