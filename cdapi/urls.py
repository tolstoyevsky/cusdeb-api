"""cdapi URL Configuration. """

from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [  # pylint: disable=invalid-name
    path('admin/', admin.site.urls),
    re_path('api/(?P<version>(v1|v2))/auth/', include('users.urls')),
    re_path('api/(?P<version>(v1|v2))/images/', include('images.urls')),
]
