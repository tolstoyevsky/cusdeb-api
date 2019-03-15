"""URL configuration for the CusDeb API Users application. """

from django.urls import re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import SignUpView, GetTokenForSocial


urlpatterns = [  # pylint: disable=invalid-name
    re_path('signup/?$', SignUpView.as_view(), name='sign-up'),
    re_path('token/?$', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    re_path('token/refresh/?$', TokenRefreshView.as_view(), name='token-refresh'),
    re_path('token/social/?$', GetTokenForSocial.as_view(),
            name='token-obtain-pair-social'),
]
