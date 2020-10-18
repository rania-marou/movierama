from rest_framework import generics

from api.models import User
from api.serializers.user import UserSerializer


class UserListCreate(generics.ListCreateAPIView):
    """
    get:
        Returns all registered users

        Publicly accessible: Yes
        Default ordering: created date (DESC)
        Available ordering: first_name, last_name, created

    post:
        Registers a new user

        Publicly accessible: Yes
        Required parameters: first_name, last_name, username, email, password
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    ordering = ('-created',)
    ordering_fields = ('first_name', 'last_name', 'created')


class UserDetail(generics.RetrieveAPIView):
    """
    get:
        Retrieves the requested user

        Publicly accessible: Yes
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
