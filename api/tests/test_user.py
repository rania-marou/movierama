from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import User


class UserTests(APITestCase):
    """
    TestCase class that exercises the User API Resource
    """

    def setUp(self) -> None:
        """
        Initial test-suite setup
        """

        # Create users
        self.user1 = User.objects.create(first_name="John", last_name="Doe", username="john", email="john@mr.com",
                                         password="Testing-123")
        self.user2 = User.objects.create(first_name="Jane", last_name="Doe", username="jane", email="jane@mr.com",
                                         password="Testing-123")

    def tearDown(self):
        """
        Handle end of test-runs
        """

        User.objects.all().delete()

    def test_user_list(self):
        """
        Test GET: /api/users/
        """

        url = reverse('user_list_create')

        # Make sure the endpoint is publicly accessible and returns two users
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Make sure we get the correct ordering
        response = self.client.get(url + "?ordering=first_name", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["first_name"], self.user2.first_name)
        self.assertEqual(response.data[1]["first_name"], self.user1.first_name)

        # Make sure all expected fields are in response
        user_fields = ('id', 'first_name', 'last_name', 'username', 'email')
        self.assertTrue(all(k in response.data[0] for k in user_fields), 'Missing field from user serializer')

    def test_user_retrieve(self):
        """
        Test GET: /api/users/<id>
        """

        url = reverse('user_retrieve', kwargs={'pk': self.user1.pk})

        # Make sure the endpoint is publicly accessible and returns all expected fields
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user1.pk)
        user_fields = ('id', 'first_name', 'last_name', 'username', 'email')
        self.assertTrue(all(k in response.data for k in user_fields), 'Missing field from user serializer')

        # Make sure the password is not returned
        self.assertNotIn('password', response.data)

        # Make sure we get 404 when requested user does not exist
        url = reverse('user_retrieve', kwargs={'pk': 0})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_create(self):
        """
        Test POST: /api/users
        """

        url = reverse('user_list_create')

        # Make sure the endpoint is publicly accessible and creates a new user
        data = {
            "username": "jenny",
            "first_name": "Jenny",
            "last_name": "Doe",
            "email": "jenny@mr.com",
            "password": "Testing-123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

        # Make sure we have all required fields
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)
