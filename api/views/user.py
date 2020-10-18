from rest_framework import generics

from api.models import User
from api.serializers.user import UserSerializer


class UserListCreate(generics.ListCreateAPIView):
    """
    list:
        Return all users, ordered by created date

    create:
        Create new user
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    ordering = ('-created',)
    ordering_fields = ('first_name', 'last_name', 'created')


class UserDetail(generics.RetrieveAPIView):
    """
    retrieve:
        Retrieve the user
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
