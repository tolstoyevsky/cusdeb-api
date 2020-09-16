"""Module containing the class-based views related to creating and managing accounts in CusDeb. """

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from social_core.actions import do_auth, do_complete, do_disconnect
from social_core.utils import setting_name
from social_django.views import _do_login

from .serializers import (
    CurrentUserSerializer,
    SocialTokenObtainPairSerializer,
    UserLoginUpdateSerializer,
    UserProfileDeleteSerializer,
)
from .utils import psa


NAMESPACE = getattr(settings, setting_name('URL_NAMESPACE'), None) or 'social'


class SignUpView(generics.CreateAPIView):
    """Creates a User model instance. """

    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        email = request.data.get('email', '')
        data = {}

        if not username:
            data[11] = 'Username cannot be empty'

        if not password:
            data[12] = 'Password cannot be empty'

        if not email:
            data[13] = 'Email cannot be empty'

        if User.objects.filter(username__iexact=username).exists():
            data[21] = 'Username is already in use'

        if User.objects.filter(email__iexact=email).exists():
            data[22] = 'Email is already in use'

        if data:
            return Response(
                data=data,
                status=status.HTTP_400_BAD_REQUEST
            )

        User.objects.create_user(username=username, password=password, email=email)

        return Response(status=status.HTTP_201_CREATED)


class WhoAmIView(generics.RetrieveAPIView):
    """Returns the name of the authenticated user the request is sent on behalf of. """

    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class GetTokenForSocial(View):
    """
    GET auth/token/social/'
    """

    def get(self, request, *_args, **_kwargs):
        """GET-method for getting social token. """
        serializer = SocialTokenObtainPairSerializer(
            data={'username': request.user.username}
        )
        if serializer.is_valid():
            return JsonResponse(serializer.validated_data, status=200)
        return JsonResponse(serializer.errors, status=400)


class UserLoginUpdate(generics.CreateAPIView):
    """Update the current user login (either username or password). """

    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        email = request.data.get('email', '')

        serializer = UserLoginUpdateSerializer(
            data={'username': username, 'email': email},
            current_user_id=request.user.id,
        )

        if serializer.is_valid():
            request.user.username = serializer.validated_data['username']
            request.user.email = serializer.validated_data['email']
            request.user.save(update_fields=['username', 'email'])

            return Response(status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDelete(generics.CreateAPIView):
    """Delete the current user profile. """

    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        serializer = UserProfileDeleteSerializer(
            data={'username': username, 'password': password},
            current_user=request.user,
        )

        if serializer.is_valid():
            request.user.delete()

            return Response(status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@never_cache
@psa(f'{NAMESPACE}:complete')
def auth(request, _backend):
    """Social authentication view. """
    return do_auth(request.backend, redirect_name=REDIRECT_FIELD_NAME)


@never_cache
@csrf_exempt
@psa(f'{NAMESPACE}:complete')
def complete(request, _backend, *args, **kwargs):
    """Authentication complete view. """
    return do_complete(request.backend, _do_login, user=request.user,
                       redirect_name=REDIRECT_FIELD_NAME, request=request, *args, **kwargs)


@never_cache
@login_required
@psa()
@require_POST
@csrf_protect
def disconnect(request, _backend, association_id=None):
    """Disconnects given backend from current logged in user. """
    return do_disconnect(request.backend, request.user, association_id,
                         redirect_name=REDIRECT_FIELD_NAME)
