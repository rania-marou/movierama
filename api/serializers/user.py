from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer for list, create and retrieve
    """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create user
        """

        # Hash the password before saving the user
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)
