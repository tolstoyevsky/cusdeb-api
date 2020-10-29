"""Module containing serializers for the CusDeb API Images application. """

from django.db.models import Q
from rest_framework import serializers

from .models import Device, Image, OS, BuildType, BuildTypeName


class OSSerializer(serializers.ModelSerializer):
    """Serializes an OS. """

    full_name = serializers.SerializerMethodField()
    short_name = serializers.SerializerMethodField()
    packages_url = serializers.StringRelatedField()
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
        fields = ('id', 'full_name', 'short_name', 'build_type', 'packages_url', )


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

    flavour = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('image_id', 'device_name', 'distro_name', 'flavour', 'started_at', 'status',
                  'notes', )

    def get_flavour(self, obj):  # pylint: disable=no-self-use
        """Returns the image flavour. """

        return obj.get_flavour_display()

    def get_status(self, obj):  # pylint: disable=no-self-use
        """Returns the image status. """

        return obj.get_status_display()


class ImageNotesUpdateSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """Serializes both the image_id and the notes provided by the current user to update their
    image notes. """

    image_id = serializers.UUIDField()
    notes = serializers.CharField(allow_blank=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('current_user')

        super().__init__(*args, **kwargs)

    def validate_image_id(self, value):  # pylint: disable=no-self-use
        """Validates if image with image_id exist and the current user has updated image. """

        try:
            image = Image.objects.get(image_id=value)
        except Image.DoesNotExist as does_not_exist:
            raise serializers.ValidationError('Image does not exist.') from does_not_exist

        if image.user != self.user:
            raise serializers.ValidationError('Current user does not have current image.')

        return value
