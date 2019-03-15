"""CusDeb API URL Configuration. """

from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [  # pylint: disable=invalid-name
    path('admin/', admin.site.urls),
    re_path('api/(?P<version>(v1|v2))/auth/', include('users.auth_urls')),
    re_path('api/(?P<version>(v1|v2))/social/', include('users.social_urls')),
    re_path('api/(?P<version>(v1|v2))/users/', include('users.users_urls')),
    re_path('api/(?P<version>(v1|v2))/init/', include('images.init_urls')),
    re_path('api/(?P<version>(v1|v2))/images/', include('images.urls')),
    path('', include('social_django.urls')),
]
