"""Module containing serializers for the CusDeb API Images application. """

from rest_framework import serializers

from .models import Image


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


class ImageDeleteSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """Serializes the image_id provided by the current user to delete their image. """

    image_id = serializers.UUIDField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('current_user')

        super().__init__(*args, **kwargs)

    def validate_image_id(self, value):  # pylint: disable=no-self-use
        """Validates if image with image exist and the current user has deleted image. """

        try:
            image = Image.objects.get(image_id=value)
        except Image.DoesNotExist as does_not_exist:
            raise serializers.ValidationError('Image does not exist.') from does_not_exist

        if image.user != self.user:
            raise serializers.ValidationError('Current user does not have current image.')

        return value


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
