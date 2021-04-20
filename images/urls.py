"""URL configuration for the CusDeb API Images application. """

from django.urls import re_path

from .views import ImageDeleteView, ImageDetailView, ImageNotesUpdateView, ListImagesView


urlpatterns = [  # pylint: disable=invalid-name
    re_path('all/?$', ListImagesView.as_view(), name='images-all'),
    re_path('delete/', ImageDeleteView.as_view(), name='image-delete'),
    re_path('update_notes/$', ImageNotesUpdateView.as_view(), name='image-notes-update'),
    re_path('image_detail/(?P<image_id>[0-9a-f-]+)/$', ImageDetailView.as_view(),
            name='image-detail'),
]
