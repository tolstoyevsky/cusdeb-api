import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status


class AuthSigningUpAndSigningInUserTest(APITestCase):
    def __init__(self, *args, **kwargs):
        super(AuthSigningUpAndSigningInUserTest, self).__init__(*args,
                                                                **kwargs)
        self._user = {
            'username': 'test.user',
            'password': 'secret',
            'email': 'test.user@domain.com',
        }

    def setUp(self):
        User.objects.create_user(**self._user)

    def test_creating_new_account(self):
        url = reverse('sign-up', kwargs={'version': 'v1'})
        user = {
            'username': 'some.username',
            'password': 'secret',
            'email': 'some.username@domain.com',
        }

        response = self.client.post(url, data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creating_new_account_with_already_taken_username(self):
        url = reverse('sign-up', kwargs={'version': 'v1'})
        error_message = {'message': 'username is already in use'}
        response = self.client.post(url, data=json.dumps(self._user),
                                    content_type='application/json')

        self.assertEqual(response.data, error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_new_account_with_already_taken_email(self):
        url = reverse('sign-up', kwargs={'version': 'v1'})
        error_message = {'message': 'email is already in use'}
        user = self._user.copy()
        user['username'] = 'some.unique.username'

        response = self.client.post(url, data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.data, error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_new_account_without_required_data(self):
        url = reverse('sign-up', kwargs={'version': 'v1'})
        error_message = {
            'message': 'username, password and email are required to sign up '
                       'a user'
        }

        user = {
            'username': 'some.username',
            'password': 'secret',
        }

        response = self.client.post(url, data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.data, error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user = {
            'username': 'some.username',
            'email': 'some.username@domain.com',
        }

        response = self.client.post(url, data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.data, error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user = {
            'password': 'secret',
            'email': 'some.username@domain.com',
        }

        response = self.client.post(url, data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.data, error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(url, data=json.dumps({}),
                                    content_type='application/json')

        self.assertEqual(response.data, error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signing_in_user(self):
        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(self._user),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_handling_non_existent_account(self):
        user = self._user.copy()
        user['username'] = 'non.existent.user'
        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        error_message = {
            'non_field_errors': [
                'No active account found with the given credentials'
            ]
        }
        response = self.client.post(url, data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.data, error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
