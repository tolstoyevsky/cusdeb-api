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
        fields = ('username', 'email', )


class SocialTokenObtainPairSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """Serializes the token data for social user. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = None

        self.fields['username'] = serializers.CharField()

    def validate(self, attrs):
        data = super().validate(attrs)

        self.user = User.objects.get(username=data['username'])

        if not self.user.is_active:
            raise serializers.ValidationError(
                ('No active account found with the given credentials'),
            )

        refresh = RefreshToken.for_user(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)  #pylint: disable=no-member

        data.pop('username')

        return data


class UserLoginUpdateSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """Serializes both the username and password provided by the current user to update their
    login (either username or email).
    """

    username = serializers.CharField()
    email = serializers.EmailField()

    def __init__(self, *args, **kwargs):
        current_user_id = kwargs.pop('current_user_id')
        self.users = User.objects.exclude(id=current_user_id)

        super().__init__(*args, **kwargs)

    def validate_username(self, value):
        """Validates the username of the current user. """

        if self.users.filter(username__iexact=value).exists():
            raise serializers.ValidationError('Username is already in use.')

        return value

    def validate_email(self, value):
        """Validates the email of the current user. """

        if self.users.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Email is already in use.')

        return value
