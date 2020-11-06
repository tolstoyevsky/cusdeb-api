"""Module containing the class-based views related to the CusDeb API Images application. """

from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status

from .models import Device, Image
from .serializers import (
    DeviceSerializer,
    ImageDeleteSerializer,
    ImageNotesUpdateSerializer,
    ImageSerializer,
)


class ListDevicesView(generics.ListAPIView):
    """Returns the list of devices supported by CusDeb. """

    queryset = Device.objects.filter(active=True)
    serializer_class = DeviceSerializer


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
