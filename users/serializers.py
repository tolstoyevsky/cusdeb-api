"""Module containing serializers for the CusDeb API Users application. """

from django.contrib.auth.models import User
from rest_framework import serializers


class TokenSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """Serializes the token data. """
    token = serializers.CharField(max_length=255)


class CurrentUserSerializer(serializers.ModelSerializer):
    """Serializes the username of the authenticated user for the whoami endpoint. """

    class Meta:
        model = User
        fields = ('username', )
