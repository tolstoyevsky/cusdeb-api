"""
Module indented to extend and override settings.py via the environment
variables.
"""

import os

from datetime import timedelta

from cdapi.settings import *  # pylint: disable=unused-wildcard-import,wildcard-import

ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS', '127.0.0.1')]

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
