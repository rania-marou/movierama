from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import User, Movie, Vote


class MovieTests(APITestCase):
    """
    TestCase class that exercises the Movie API Resource
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

        # Create movies
        self.movie1 = Movie.objects.create(title="Madagascar", description="Animation", user=self.user1)
        self.movie2 = Movie.objects.create(title="Ice Age", description="Animation", user=self.user2)

        # Create Vote
        Vote.objects.create(movie=self.movie1, user=self.user2, reaction=Vote.SupportedMovieVotes.LIKE)

    def tearDown(self):
        """
        Handle end of test-runs
        """

        User.objects.all().delete()
        Movie.objects.all().delete()
        Vote.objects.all().delete()

    def test_movie_list(self):
        """
        Test GET: /api/movies/
        """

        url = reverse('movie_list_create')

        # Make sure the endpoint is publicly accessible and returns two movies
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Make sure all expected fields are in response
        user_fields = ('id', 'title', 'description', 'created', 'user', 'likes', 'hates', 'vote')
        self.assertTrue(all(k in response.data[0] for k in user_fields), 'Missing field from movie serializer')

        # Make sure we get the correct ordering
        response = self.client.get(url + "?ordering=title", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], self.movie2.title)
        self.assertEqual(response.data[1]["title"], self.movie1.title)
        response = self.client.get(url + "?ordering=-likes", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], self.movie1.id)
        self.assertEqual(response.data[0]["likes"], 1)
        self.assertEqual(response.data[0]["hates"], 0)
        self.assertIsNone(response.data[0]["vote"])

        # Make sure filtering is working as expected
        response = self.client.get(url + "?user_id=" + str(self.user2.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.movie2.title)

        # Make sure user1 does not have any vote for this movie
        token = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token.access_token))
        response = self.client.get(url + "?user_id=" + str(self.user1.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data[0]["vote"])

        # Make sure user2 has a like vote for this movie
        token = RefreshToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token.access_token))
        response = self.client.get(url + "?user_id=" + str(self.user1.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["vote"], Vote.SupportedMovieVotes.LIKE)

    def test_movie_create(self):
        """
        Test POST: /api/movies
        """

        url = reverse('movie_list_create')

        # Make sure the endpoint is not publicly accessible
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Make sure that logged in users can create new movie
        token = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token.access_token))
        data = {
            "title": "Despicable Me"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 3)

        # Make sure the created movie has the correct owner
        movie = Movie.objects.get(pk=response.data['id'])
        self.assertEqual(movie.user_id, self.user1.pk)

        # Make sure that the movie title is required
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
