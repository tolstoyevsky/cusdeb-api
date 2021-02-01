"""Django config module. """

from django.apps import AppConfig
from django.conf import settings

from pieman_devices import get_devices


class ImagesConfig(AppConfig):
    """CusDeb API Images application config class. """

    name = 'images'

    def ready(self):
        settings.DEVICES_LIST = get_devices()
