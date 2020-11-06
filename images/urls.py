"""URL configuration for the CusDeb API Images application. """

from django.urls import re_path

from .views import ImageDeleteView, ImageNotesUpdateView, ListImagesView


urlpatterns = [  # pylint: disable=invalid-name
    re_path('all/?$', ListImagesView.as_view(), name='images-all'),
    re_path('delete/', ImageDeleteView.as_view(), name='image-delete'),
    re_path('update_notes/$', ImageNotesUpdateView.as_view(), name='image-notes-update'),
]
