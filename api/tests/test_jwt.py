from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import User


class JwtTests(APITestCase):
    """
    TestCase class that exercises the JWT API Resource
    """

    def setUp(self) -> None:
        """
        Initial test-suite setup
        """

        # Create users
        self.user1_password = "Testing-123"
        self.user1 = User.objects.create(first_name="John", last_name="Doe", username="john", email="john@mr.com",
                                         password=make_password(self.user1_password))

    def tearDown(self):
        """
        Handle end of test-runs
        """

        self.user1.delete()

    def test_token_retrieve(self):
        """
        Test POST: /api/token
        """

        url = reverse('token_obtain_pair')

        # Make sure the endpoint is publicly accessible and returns access & refresh tokens
        data = {
            "username": self.user1.username,
            "password": self.user1_password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Make sure the endpoint does not return tokens in case of invalid credentials
        data = {
            "username": self.user1.username,
            "password": "foo"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        """
        Test POST: /token/refresh
        """

        url = reverse('token_refresh')

        # Make sure the endpoint is publicly accessible and returns access & refresh tokens
        data = {
            "refresh": str(RefreshToken.for_user(self.user1))
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Make sure we can not refresh an expired/invalid token
        data = {
            "refresh": "invalid_token"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
