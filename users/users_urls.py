"""
URL configuration for the CusDeb API Users application (fetching user-specific information only).
"""

from django.urls import re_path, include

from .views import WhoAmIView, PasswordUpdate, UserLoginUpdate, UserProfileDelete


urlpatterns = [  # pylint: disable=invalid-name
    re_path('whoami/?$', WhoAmIView.as_view(), name='who-am-i'),
    re_path('password_reset/?', include('django_rest_passwordreset.urls',
                                        namespace='password_reset')),
    re_path('password_update/?', PasswordUpdate.as_view(), name='password-update'),
    re_path('login_update/?', UserLoginUpdate.as_view(), name='user-login-update'),
    re_path('profile_delete/?', UserProfileDelete.as_view(), name='user-profile-delete'),
]
