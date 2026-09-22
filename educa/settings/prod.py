from decouple import config
from .base import *


DEBUG = False

ADMINS = [
    ('jonadmin don', 'prodenv001@gmail.com')
]

ALLOWED_HOSTS = ['.educaproject.com']
# A value that begins with a period is used as a subdomain wildcard; '.educaproject.com' will
# match any subdomain of educaproject.com and any subdomain for this domain, for example,
# -> course.educaproject.com and django.educaproject.com.


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

# Security
CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE: Use a secure cookie for cross-site request forgery (CSRF) protection.
# With True, browsers will only transfer the cookie over HTTPS.
SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE: Use a secure session cookie. With True, browsers will only
# transfer the cookie over HTTPS
SECURE_SSL_REDIRECT = True
# SECURE_SSL_REDIRECT: This indicates whether HTTP requests have to be redirected to HTTPs.