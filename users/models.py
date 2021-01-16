"""Models for the CusDeb API Users application. """

import binascii
import os
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Person(models.Model):
    """Extends the User model. """

    user = models.OneToOneField(User, models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'


class EmailConfirmationToken(models.Model):
    """The token for email confirmation. """

    person = models.OneToOneField(Person, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(db_index=True, unique=True, max_length=8)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.token:
            self.token = binascii.hexlify(os.urandom(4)).decode()

        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    def __str__(self):
        return f'{self.token}'


def clear_expired_email_confirmation_tokens():
    """Removes all expired email confirmation tokens. """

    expiry_time = timezone.now() - timedelta(minutes=settings.EMAIL_CONFIRMATION_TOKEN_TTL)

    EmailConfirmationToken.objects.filter(created_at__lte=expiry_time).delete()
