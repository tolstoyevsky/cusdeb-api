"""Module containing a custom authentication backend. """

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CaseInsensitiveModelBackend(ModelBackend):
    """Authentication backend class that allows case-insensitive login. """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)

        try:
            username_field = f'{user_model.USERNAME_FIELD}__iexact'
            # pylint: disable=protected-access
            user = user_model._default_manager.get(**{username_field: username})
        except user_model.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (see
            # https://code.djangoproject.com/ticket/20760)
            user_model().set_password(password)

            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user)\
                    and user.person.email_confirmed:
                return user

            return None
