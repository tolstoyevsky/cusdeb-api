"""Module containing serializers for the CusDeb API Images application. """

from django.db.models import Q
from rest_framework import serializers

from .models import Device, Image, OS, BuildType, BuildTypeName


class OSSerializer(serializers.ModelSerializer):
    """Serializes an OS. """

    full_name = serializers.SerializerMethodField()
    short_name = serializers.SerializerMethodField()
    build_type = serializers.SerializerMethodField()

    def get_build_type(self, obj):
        """Returns either the specified build types (if any) or a build type by default. """

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

    def get_full_name(self, obj):  # pylint: disable=no-self-use
        """Returns the full name of the operating system intended for a client. """

        return str(OS.objects.get(pk=obj.id))

    def get_short_name(self, obj):  # pylint: disable=no-self-use
        """Returns the short name of the operating system intended for Pieman. """

        return str(OS.objects.get(pk=obj.id).get_short_name())

    class Meta:
        model = OS
        fields = ('id', 'full_name', 'short_name', 'build_type', )


class DeviceSerializer(serializers.ModelSerializer):
    """Serializes a device. """

    name = serializers.StringRelatedField()
    os = serializers.SerializerMethodField()

    def get_os(self, obj):  # pylint: disable=no-self-use
        """Returns the list of OSes available for the device. """

        queryset = obj.supported_os.all()
        return OSSerializer(queryset, many=True, context={'device_id': obj.id}).data

    class Meta:
        model = Device
        fields = ('id', 'name', 'generation', 'model', 'os', )


class ImageSerializer(serializers.ModelSerializer):
    """Serializes an image. """

    device = DeviceSerializer()
    os = OSSerializer()
    build_type = serializers.StringRelatedField()

    class Meta:
        model = Image
        fields = ('device', 'os', 'build_type', 'started_at', 'status',
                  'format', 'finished_at', 'notes', )
