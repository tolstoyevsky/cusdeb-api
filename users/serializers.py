"""Module containing serializers for the CusDeb API Users application. """

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class TokenSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """Serializes the token data. """
    token = serializers.CharField(max_length=255)


class CurrentUserSerializer(serializers.ModelSerializer):
    """Serializes the username of the authenticated user for the whoami endpoint. """

    class Meta:
        model = User
        fields = ('username', )


class SocialTokenObtainPairSerializer(serializers.Serializer):
    """Serializes the token data for social user. """
    def __init__(self, *args, **kwargs):
        super(SocialTokenObtainPairSerializer, self).__init__(*args, **kwargs)

        self.fields['username'] = serializers.CharField()

    def validate(self, attrs):
        data = super(SocialTokenObtainPairSerializer, self).validate(attrs)

        self.user = User.objects.get(username=data['username'])

        if not self.user.is_active:
            raise serializers.ValidationError(
                ('No active account found with the given credentials'),
            )

        refresh = RefreshToken.for_user(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        data.pop('username')

        return data
