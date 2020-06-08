"""Data models for the CusDeb API Users application. """
import binascii
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    """Extends user model"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='related user',
    )
    email_confirmed = models.BooleanField(default=False)


class EmailConfirmationToken(models.Model):
    """Token for email confirmed"""

    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        verbose_name='related person'
    )
    created_at = models.DateField(auto_now_add=True)
    key = models.CharField(db_index=True, unique=True, max_length=64)

    def save(self, *args, **kwargs):
        # pylint: disable=W0222
        if not self.key:
            self.key = binascii.hexlify(os.urandom(32)).decode()

        return super(EmailConfirmationToken, self).save(*args, **kwargs)


def get_email_confirmation_token_expiry_time():
    """
    Returns the email confirmation token expiry time in hours (default: 24)
    Set Django SETTINGS.DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME to overwrite this time
    :return: expiry time
    """
    # get token validation time
    return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME', 24)


def clear_expired(expiry_time):
    """
    Remove all expired tokens
    :param expiry_time: Token expiration time
    """
    # pylint: disable=no-member
    EmailConfirmationToken.objects.filter(created_at__lte=expiry_time).delete()
