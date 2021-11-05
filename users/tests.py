"""Tests for the CusDeb API Users application. """

import json
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail
from rest_framework.views import status

from util.base_test import BaseSingleUserTest


class AuthSigningUpAndSigningInUserTest(BaseSingleUserTest):
    """Tests signing up/in. """

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
        error_message = {
            21: 'Username is already in use',
            22: 'Email is already in use',
        }
        response = self.client.post(url, data=json.dumps(self._user),
                                    content_type='application/json')

        self.assertEqual(response.data, error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_new_account_with_already_taken_email(self):
        url = reverse('sign-up', kwargs={'version': 'v1'})
        error_message = {22: 'Email is already in use'}
        user = self._user.copy()
        user['username'] = 'some.unique.username'

        response = self.client.post(url, data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.data, error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_new_account_without_required_data(self):
        url = reverse('sign-up', kwargs={'version': 'v1'})
        error_message = {13: 'Email cannot be empty'}

        user = {
            'username': 'some.username',
            'password': 'secret',
        }

        response = self.client.post(url, data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.data, error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error_message = {12: 'Password cannot be empty'}

        user = {
            'username': 'some.username',
            'email': 'some.username@domain.com',
        }

        response = self.client.post(url, data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.data, error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error_message = {11: 'Username cannot be empty'}

        user = {
            'password': 'secret',
            'email': 'some.username@domain.com',
        }

        response = self.client.post(url, data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.data, error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error_message = {
            11: 'Username cannot be empty',
            12: 'Password cannot be empty',
            13: 'Email cannot be empty',
        }

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
            'detail': ErrorDetail(
                string='No active account found with the given credentials',
                code='no_active_account',
            ),
        }
        response = self.client.post(url, data=json.dumps(user),
                                    content_type='application/json')

        self.assertEqual(response.data, error_message)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class WhoAmIUserTest(BaseSingleUserTest):
    """Tests the whoami endpoint. """

    def test_whoami(self):
        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        response_content = b'{"username":"test.user","email":"test.user@domain.com"}'
        auth = self.client.post(url, data=json.dumps(self._user),
                                content_type='application/json')

        # pylint: disable=no-member
        fake_header = b'Bearer ' + json.loads(auth.content)['access'].encode()
        url = reverse('who-am-i', kwargs={'version': 'v1'})
        response = self.client.get(url, content_type='application/json',
                                   HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.content, response_content)

    def test_whoami_unauthorized(self):
        url = reverse('who-am-i', kwargs={'version': 'v1'})
        response = self.client.get(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PasswordUpdateTest(BaseSingleUserTest):
    """Tests the password_update endpoint. """

    def test_password_update(self):
        """Tests if it's possible to update the current user password. """

        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        auth = self.client.post(url, data=json.dumps(self._user), content_type='application/json')
        fake_header = b'Bearer ' + json.loads(auth.content)['access'].encode()

        password = 'SuperSecret'
        data = {
            'old_password': self._user['password'],
            'password': password,
            'retype_password': password,
        }
        url = reverse('password-update', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_update_with_missing_fields(self):
        """Tests if it's not possible to update the current user password when the required fields
        are partially missing.
        """

        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        auth = self.client.post(url, data=json.dumps(self._user), content_type='application/json')
        fake_header = b'Bearer ' + json.loads(auth.content)['access'].encode()

        password = 'SuperSecret'
        data = {
            'password': password,
            'retype_password': password,
        }
        url = reverse('password-update', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.content, b'{"old_password": ["This field may not be blank."]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'old_password': self._user['password'],
            'retype_password': password,
        }
        url = reverse('password-update', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.content, b'{"password": ["This field may not be blank."]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'old_password': self._user['password'],
            'password': password,
        }
        response_content = (b'{"password": ["Passwords mismatch."], '
                            b'"retype_password": ["This field may not be blank."]}')
        url = reverse('password-update', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.content, response_content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_update_with_incorrect_old_password(self):
        """"Tests if it's not possible to update the current user password with incorrect
        old password.
        """

        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        auth = self.client.post(url, data=json.dumps(self._user), content_type='application/json')
        fake_header = b'Bearer ' + json.loads(auth.content)['access'].encode()

        password = 'SuperSecret'
        data = {
            'old_password': self._user['password'] * 2,
            'password': password,
            'retype_password': password,
        }
        url = reverse('password-update', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.content, b'{"old_password": ["Incorrect old password."]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_update_when_passwords_mismatch(self):
        """"Tests if it's not possible to update the current user password when the old and
        new passwords mismatch.
        """

        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        auth = self.client.post(url, data=json.dumps(self._user), content_type='application/json')
        fake_header = b'Bearer ' + json.loads(auth.content)['access'].encode()

        data = {
            'old_password': self._user['password'],
            'password': 'SuperSecret',
            'retype_password': 'SuperSecret1',
        }
        url = reverse('password-update', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.content, b'{"password": ["Passwords mismatch."]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_update_with_invalid_new_password(self):
        """"Tests if it's not possible to update the current user password when the new one is
        invalid. The new password is considered as 'invalid' when
        * it contains less than 8 characters;
        * it's too common.
        """

        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        auth = self.client.post(url, data=json.dumps(self._user), content_type='application/json')
        fake_header = b'Bearer ' + json.loads(auth.content)['access'].encode()

        data = {
            'old_password': self._user['password'],
            'password': 'secret',
            'retype_password': 'secret',
        }
        response_content = (b'{"password": ["This password is too short. It must contain at least '
                            b'8 characters.", "This password is too common."]}')
        url = reverse('password-update', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.content, response_content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_update_unauthorized(self):
        """Tests if it's not possible to update a password when unauthorized. """

        url = reverse('password-update', kwargs={'version': 'v1'})
        response = self.client.post(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserLoginUpdateTest(BaseSingleUserTest):
    """Tests the profile_update endpoint. """

    def test_user_login_update(self):
        """Tests if it's possible to update the current user login (either username or email). """

        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        auth = self.client.post(url, data=json.dumps(self._user), content_type='application/json')
        fake_header = b'Bearer ' + json.loads(auth.content)['access'].encode()

        data = {
            'username': 'new_username',
            'email': 'new_email@cusdeb.com',
        }
        url = reverse('user-login-update', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_update_with_missing_fields(self):
        """Tests if it's not possible to update the current user login (either username or email)
        when the required fields are partially missing. It must be provided both username and email
        to update one of them.
        """

        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        auth = self.client.post(url, data=json.dumps(self._user), content_type='application/json')
        fake_header = b'Bearer ' + json.loads(auth.content)['access'].encode()

        data = {'email': 'new_email@cusdeb.com'}
        url = reverse('user-login-update', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.content, b'{"username": ["This field may not be blank."]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'username': 'new_username'}
        url = reverse('user-login-update', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.content, b'{"email": ["This field may not be blank."]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_update_using_already_taken_username_or_email(self):
        """Tests if it's not possible to update the current user login using already taken username
        or email.
        """

        data = {
            'username': 'new_username',
            'email': 'new_email@cusdeb.com',
        }
        user = {
            **data,
            'password': 'secret',
        }
        User.objects.create_user(**user)

        response_content = (b'{"username": ["Username is already in use."], '
                            b'"email": ["Email is already in use."]}')

        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        auth = self.client.post(url, data=json.dumps(self._user), content_type='application/json')
        fake_header = b'Bearer ' + json.loads(auth.content)['access'].encode()

        url = reverse('user-login-update', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.content, response_content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_update_unauthorized(self):
        """Tests if it's not possible to update a login (either username or email) when
        unauthorized.
        """

        url = reverse('user-login-update', kwargs={'version': 'v1'})
        response = self.client.post(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileDeleteTest(BaseSingleUserTest):
    """Tests the profile_delete endpoint. """

    def test_user_profile_delete(self):
        """Tests if it's possible to delete the current user profile. """

        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        auth = self.client.post(url, data=json.dumps(self._user), content_type='application/json')
        fake_header = b'Bearer ' + json.loads(auth.content)['access'].encode()

        data = self._user.copy()
        url = reverse('user-profile-delete', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_delete_when_unconfirmed(self):
        """Tests if it's not possible to delete the current user profile when the required fields
        are partially missing. The user must confirm the deletion by typing their username and
        password.
        """

        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        auth = self.client.post(url, data=json.dumps(self._user), content_type='application/json')
        fake_header = b'Bearer ' + json.loads(auth.content)['access'].encode()

        data = {'password': self._user['password']}
        url = reverse('user-profile-delete', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.content, b'{"username": ["This field may not be blank."]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'username': self._user['username']}
        url = reverse('user-profile-delete', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.content, b'{"password": ["This field may not be blank."]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_profile_delete_when_unconfirmed2(self):
        """Tests if it's not possible to delete the user profile when unconfirmed. The user must
        confirm the deletion by typing their username and password.
        """

        url = reverse('token-obtain-pair', kwargs={'version': 'v1'})
        auth = self.client.post(url, data=json.dumps(self._user), content_type='application/json')
        fake_header = b'Bearer ' + json.loads(auth.content)['access'].encode()

        data = {
            'username': self._user['username'] * 2,
            'password': self._user['password'] * 2,
        }
        response_content = (b'{"username": ["Username mismatch."], '
                            b'"password": ["Incorrect password."]}')
        url = reverse('user-profile-delete', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=fake_header)

        self.assertEqual(response.content, response_content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_profile_delete_unauthorized(self):
        """Tests if it's not possible to delete a user profile when unauthorized. """

        url = reverse('user-profile-delete', kwargs={'version': 'v1'})
        response = self.client.post(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserConfirmEmailTest(BaseSingleUserTest):
    """Tests the confirm_email endpoint. """

    def test_confirm_email(self):
        """Test if it's possible to confirm the user email. """

        user = User.objects.get(username=self._user['username'])
        user.person.email_confirmed = False
        user.person.save(update_fields=['email_confirmed'])
        email_confirmation_token = user.person.emailconfirmationtoken.token

        url = reverse('confirm-email', kwargs={'version': 'v1'})
        data = {'token': email_confirmation_token}
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_confirm_email_with_invalid_token(self):
        """Tests if it's not possible to confirm the user email with invalid token. """

        url = reverse('confirm-email', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps({'token': 'invalid_token'}),
                                    content_type='application/json')

        self.assertEqual(response.content,
                         b'{"token": ["Ensure this field has no more than 8 characters."]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_confirm_email_with_already_confirmed_email(self):
        """Tests if it's not possible to confirm an already confirmed email. """

        user = User.objects.get(username=self._user['username'])
        email_confirmation_token = user.person.emailconfirmationtoken.token
        user.person.emailconfirmationtoken.delete()

        url = reverse('confirm-email', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps({'token': email_confirmation_token}),
                                    content_type='application/json')

        self.assertEqual(response.content, b'{"token": ["Token doesn\'t exist."]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_confirm_email_with_expired_token(self):
        """Tests if it's not possible to confirm the user email with an expired token. """

        user = User.objects.get(username=self._user['username'])
        user.person.email_confirmed = False
        user.person.save(update_fields=['email_confirmed'])

        email_confirmation_token = user.person.emailconfirmationtoken.token
        user.person.emailconfirmationtoken.created_at = timezone.now() - timedelta(
            minutes=settings.EMAIL_CONFIRMATION_TOKEN_TTL)
        user.person.emailconfirmationtoken.save(update_fields=['created_at'])

        url = reverse('confirm-email', kwargs={'version': 'v1'})
        response = self.client.post(url, data=json.dumps({'token': email_confirmation_token}),
                                    content_type='application/json')

        self.assertEqual(response.content, b'{"token": ["Token doesn\'t exist."]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
