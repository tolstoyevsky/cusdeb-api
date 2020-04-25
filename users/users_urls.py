"""
URL configuration for the CusDeb API Users application (fetching user-specific information only).
"""

from django.urls import re_path, include

from .views import WhoAmIView


urlpatterns = [  # pylint: disable=invalid-name
    re_path('whoami/?$', WhoAmIView.as_view(), name='who-am-i'),
    re_path('password_reset/?', include('django_rest_passwordreset.urls',
                                        namespace='password_reset')),
]
