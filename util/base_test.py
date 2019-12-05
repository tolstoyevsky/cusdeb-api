from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class BaseSingleUserTest(APITestCase):
    def __init__(self, *args, **kwargs):
        super(BaseSingleUserTest, self).__init__(*args, **kwargs)
        self._user = {
            'username': 'test.user',
            'password': 'secret',
            'email': 'test.user@domain.com',
        }

    def setUp(self):
        User.objects.create_user(**self._user)
