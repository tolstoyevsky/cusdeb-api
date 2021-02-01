"""Module for the admin interface of the application. """

from django.contrib import admin

from .models import Image


admin.site.register(Image)
