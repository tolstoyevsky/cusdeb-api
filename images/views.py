from rest_framework import generics, permissions

from .models import Device, Image
from .serializers import (
    DeviceSerializer,
    ImageSerializer,
)


class ListDevicesView(generics.ListAPIView):
    queryset = Device.objects.filter(active=True)
    serializer_class = DeviceSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ListImagesView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, )
