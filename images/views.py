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
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Image.objects.filter(user=user)
