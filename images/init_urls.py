from django.urls import re_path

from .views import ListDevicesView


urlpatterns = [  # pylint: disable=invalid-name
    re_path('list_devices/?$', ListDevicesView.as_view(), name='list-devices'),
]
