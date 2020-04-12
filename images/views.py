"""Module containing the class-based views related to the CusDeb API Images application. """

from rest_framework import generics, permissions

from .models import Device, Image
from .serializers import (
    DeviceSerializer,
    ImageSerializer,
)


class ListDevicesView(generics.ListAPIView):
    """Returns the list of devices supported by CusDeb. """

    queryset = Device.objects.filter(active=True)
    serializer_class = DeviceSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ListImagesView(generics.ListAPIView):
    """Returns the list of images which belong to the authenticated user. """

    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Image.objects.filter(user=user)
