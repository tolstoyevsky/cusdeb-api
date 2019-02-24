from rest_framework import generics
from rest_framework import permissions

from .models import Image
from .serializers import ImageSerializer


class ListImagesView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, )
