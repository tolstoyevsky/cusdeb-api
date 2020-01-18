from django.db.models import Q
from rest_framework import serializers

from .models import Device, Image, OS, BuildType, BuildTypeName


class OSSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    codename = serializers.StringRelatedField()
    port = serializers.StringRelatedField()
    build_type = serializers.SerializerMethodField()

    def get_build_type(self, obj):
        device_id = self.context.get('device_id')
        build_types = BuildType.objects.filter(
            Q(device=device_id) &
            Q(os=obj.id)
        ).values_list('build_type__name', flat=True)
        if build_types:
            return build_types

        # If there are no build types associated with the OS, use the first one
        # (i.e. pk=1) by default.
        return [BuildTypeName.objects.get(pk=1).name]

    class Meta:
        model = OS
        fields = ('id', 'name', 'codename', 'version', 'port', 'build_type', )


class DeviceSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    os = serializers.SerializerMethodField()

    def get_os(self, obj):
        queryset = obj.supported_os.all()
        return OSSerializer(queryset, many=True, context={
            'device_id': obj.id,
        }).data

    class Meta:
        model = Device
        fields = ('id', 'name', 'generation', 'model', 'os', )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('name', )
