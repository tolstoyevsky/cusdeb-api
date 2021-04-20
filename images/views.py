"""Module containing the class-based views related to the CusDeb API Images application. """

from django.conf import settings
from django.http import JsonResponse
from django.views import View
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status

from .models import Image
from .serializers import (
    ImageDeleteSerializer,
    ImageDetailSerializer,
    ImageNotesUpdateSerializer,
    ImageSerializer,
)


class ListDevicesView(View):
    """Returns the list of devices supported by CusDeb. """

    def get(self, *_args, **_kwargs):
        """GET-method for receiving devices list. """

        return JsonResponse(settings.DEVICES_LIST)


class ListImagesView(generics.ListAPIView):
    """Returns the list of images which belong to the authenticated user. """

    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Image.objects.filter(user=user)


class ImageDeleteView(generics.DestroyAPIView):
    """Deletes an image. """

    permission_classes = (permissions.IsAuthenticated, )

    def delete(self, request, *args, **kwargs):
        image_id = request.data.get('image_id', '')

        serializer = ImageDeleteSerializer(
            data={'image_id': image_id},
            current_user=request.user,
        )

        if serializer.is_valid():
            Image.objects.filter(image_id=image_id).delete()
            return Response(status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetailView(generics.RetrieveAPIView):
    """Returns the image which belong to the authenticated user. """

    serializer_class = ImageDetailSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'image_id'

    def get_queryset(self):
        user = self.request.user
        return Image.objects.filter(user=user)


class ImageNotesUpdateView(generics.UpdateAPIView):
    """Update image notes. """

    permission_classes = (permissions.IsAuthenticated, )

    def put(self, request, *args, **kwargs):
        image_id = request.data.get('image_id', '')
        notes = request.data.get('notes', '')

        serializer = ImageNotesUpdateSerializer(
            data={'image_id': image_id, 'notes': notes},
            current_user=request.user,
        )

        if serializer.is_valid():
            Image.objects.filter(image_id=image_id).update(notes=notes)
            return Response(status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
