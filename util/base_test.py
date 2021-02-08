"""Module containing common code that might be shared between different test modules. """

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from images.models import Image


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


class BaseImageTest(BaseSingleUserTest):
    """Base class for the image tests that need to have an images created before running. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user2 = {
            'username': 'test.user2',
            'password': 'secret',
            'email': 'test.user2@domain.com',
        }
        self._user_image_id = '21d43a3c-2a2c-45c1-8249-024baac7c399'
        self._user2_image_id = '438afe69-3ad7-4f50-b6e7-e82a3518171e'

    def setUp(self):
        super().setUp()

        user = User.objects.get(username=self._user['username'])
        Image.objects.create(
            user=user,
            image_id=self._user_image_id,
            device_name='Raspberry Pi 3 Model B',
            distro_name='Debian 10 "Buster" (32-bit)',
            flavour='C',
            status='S',
        )

        user2 = User.objects.create_user(**self._user2)
        Image.objects.create(
            user=user2,
            image_id=self._user2_image_id,
            device_name='Raspberry Pi 3 Model B',
            distro_name='Debian 10 "Buster" (32-bit)',
            flavour='C',
            status='S',
        )
