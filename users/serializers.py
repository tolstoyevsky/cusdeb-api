from django.contrib.auth.models import User
from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    """Serializes the token data. """
    token = serializers.CharField(max_length=255)


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )
