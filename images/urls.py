"""URL configuration for the CusDeb API Images application. """

from django.urls import re_path

from .views import ListImagesView


urlpatterns = [  # pylint: disable=invalid-name
    re_path('all/?$', ListImagesView.as_view(), name='images-all'),
]
