"""
URL configuration for the CusDeb API Users application (fetching user-specific information only).
"""

from django.urls import re_path, include

from .views import WhoAmIView, UserLoginUpdate


urlpatterns = [  # pylint: disable=invalid-name
    re_path('whoami/?$', WhoAmIView.as_view(), name='who-am-i'),
    re_path('password_reset/?', include('django_rest_passwordreset.urls',
                                        namespace='password_reset')),
    re_path('login_update/?', UserLoginUpdate.as_view(), name='user-login-update'),
]
