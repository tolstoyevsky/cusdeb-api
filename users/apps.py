"""Django config module. """

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """CusDeb API Users application config class. """

    name = 'users'

    def ready(self):
        import users.signals  # pylint: disable=unused-import,import-outside-toplevel
