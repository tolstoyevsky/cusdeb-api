"""
Module indented to extend and override settings.py via the environment
variables.
"""

import os

from datetime import timedelta

from cdapi.settings import *  # pylint: disable=unused-wildcard-import,wildcard-import

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')

DEBUG = os.getenv('DEBUG', '').lower() == 'true'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('PG_NAME', 'cusdeb-api'),
        'USER': os.getenv('PG_USER', 'postgres'),
        'PASSWORD': os.getenv('PG_PASSWORD', 'secret'),
        'HOST': os.getenv('PG_HOST', 'localhost'),
        'PORT': os.getenv('PG_PORT', '54321'),
    }
}

# Do not run anything if SECRET_KEY is not set.
SECRET_KEY = os.environ['SECRET_KEY']

TOKEN_TTL = int(os.getenv('TOKEN_TTL', '5'))

REFRESH_TOKEN_TTL = int(os.getenv('REFRESH_TOKEN_TTL', '2880'))  # 48 hours

SIMPLE_JWT['ALGORITHM'] = os.getenv('JWT_ALGORITHM', 'HS256')

SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY

SIMPLE_JWT['SLIDING_TOKEN_LIFETIME'] = timedelta(minutes=TOKEN_TTL)

SIMPLE_JWT['SLIDING_TOKEN_REFRESH_LIFETIME'] = timedelta(minutes=REFRESH_TOKEN_TTL)

SOCIAL_AUTH_GITHUB_KEY = os.getenv('SOCIAL_AUTH_GITHUB_KEY', '')

SOCIAL_AUTH_GITHUB_SECRET = os.getenv('SOCIAL_AUTH_GITHUB_SECRET', '')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', '')

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', '')

SOCIAL_AUTH_LOGIN_REDIRECT_URL = os.getenv('SOCIAL_AUTH_LOGIN_REDIRECT_URL', '/')

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')

EMAIL_PORT = int(os.getenv('EMAIL_PORT', '25'))

EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', '').lower() == 'true'

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

BASE_SITE_URL = os.getenv('BASE_SITE_URL', 'cusdeb.com')

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'info@cusdeb.com')

DEFAULT_SITE_NAME = os.getenv('DEFAULT_SITE_NAME', 'CusDeb')
