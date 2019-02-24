from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    """Serializes the token data. """
    token = serializers.CharField(max_length=255)
