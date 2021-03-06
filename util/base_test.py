"""Module containing common code that might be shared between different test modules. """

from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class BaseSingleUserTest(APITestCase):
    """Base class for the tests that need to have a user created before running. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = {
            'username': 'test.user',
            'password': 'secret',
            'email': 'test.user@domain.com',
        }

    def setUp(self):
        user = User.objects.create_user(**self._user)

        user.person.email_confirmed = True
        user.person.save(update_fields=['email_confirmed'])
