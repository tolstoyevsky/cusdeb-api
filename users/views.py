"""Module containing the class-based views related to creating and managing accounts in CusDeb. """

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status

from .serializers import CurrentUserSerializer


class SignUpView(generics.CreateAPIView):
    """Creates a User model instance. """

    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        email = request.data.get('email', '')

        if not username or not password or not email:
            return Response(
                data={'message': 'username, password and email are required '
                                 'to sign up a user'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username__iexact=username).exists():
            return Response(
                data={'message': 'username is already in use'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email__iexact=email).exists():
            return Response(
                data={'message': 'email is already in use'},
                status=status.HTTP_400_BAD_REQUEST
            )

        User.objects.create_user(username=username, password=password,
                                 email=email)

        return Response(status=status.HTTP_201_CREATED)


class WhoAmIView(generics.RetrieveAPIView):
    """Returns the name of the authenticated user the request is sent on behalf of. """

    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
