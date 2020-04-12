"""URL configuration for the CusDeb API Images application (the part related to the initialization
step only).
"""

from django.urls import re_path

from .views import ListDevicesView


urlpatterns = [  # pylint: disable=invalid-name
    re_path('list_devices/?$', ListDevicesView.as_view(), name='list-devices'),
]
