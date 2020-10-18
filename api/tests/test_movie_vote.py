from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import User, Movie, Vote


class MovieVoteTests(APITestCase):
    """
    TestCase class that exercises the Movie Vote API Resource
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
        self.user3 = User.objects.create(first_name="Jack", last_name="Doe", username="jack", email="jack@mr.com",
                                         password="Testing-123")

        # Create movies
        self.movie1 = Movie.objects.create(title="Madagascar", description="Animation", user=self.user1)
        self.movie2 = Movie.objects.create(title="Madagascar II", description="Animation", user=self.user1)
        self.movie3 = Movie.objects.create(title="Madagascar IIΙ", description="Animation", user=self.user1)
        self.movie4 = Movie.objects.create(title="Ice Age", description="Animation", user=self.user2)

        # Create Vote
        Vote.objects.create(movie=self.movie1, user=self.user2, reaction=Vote.SupportedMovieVotes.LIKE)
        Vote.objects.create(movie=self.movie2, user=self.user2, reaction=Vote.SupportedMovieVotes.HATE)
        Vote.objects.create(movie=self.movie3, user=self.user2, reaction=Vote.SupportedMovieVotes.LIKE)
        Vote.objects.create(movie=self.movie4, user=self.user1, reaction=Vote.SupportedMovieVotes.LIKE)
        Vote.objects.create(movie=self.movie3, user=self.user3, reaction=Vote.SupportedMovieVotes.HATE)
        Vote.objects.create(movie=self.movie4, user=self.user3, reaction=Vote.SupportedMovieVotes.LIKE)

    def tearDown(self):
        """
        Handle end of test-runs
        """

        User.objects.all().delete()
        Movie.objects.all().delete()
        Vote.objects.all().delete()

    def test_movie_votes_list(self):
        """
        Test GET: /api/movies/<id>/votes
        """

        url = reverse('movie_vote_list_create_update_delete', kwargs={'movie_id': self.movie3.id})

        # Make sure the endpoint is not publicly accessible
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Make sure logged in users can list movie votes
        token = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token.access_token))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Make sure all expected fields are in response
        user_fields = ('reaction', 'user', 'created')
        self.assertTrue(all(k in response.data[0] for k in user_fields), 'Missing field from movie vote serializer')

        # Make sure filtering is working as expected
        response = self.client.get(url + "?reaction=" + Vote.SupportedMovieVotes.HATE, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_movie_vote_create(self):
        """
        Test POST: /api/movies/<id>/votes
        """

        url = reverse('movie_vote_list_create_update_delete', kwargs={'movie_id': self.movie1.id})

        # Make sure the endpoint is not publicly accessible
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Login as a user and create new vote
        token = RefreshToken.for_user(self.user3)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token.access_token))
        data = {
            "reaction": Vote.SupportedMovieVotes.LIKE
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 7)

        # Make sure a logged in user can not vote twice for the same movie
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'You can not vote for this movie twice.')

        # Make sure a logged in user can not vote for a movie he/she submitted
        token = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token.access_token))
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'You can not vote for movies you submitted.')

    def test_movie_vote_update(self):
        """
        Test PATCH: /api/movies/<id>/votes
        """

        url = reverse('movie_vote_list_create_update_delete', kwargs={'movie_id': self.movie1.id})

        # Make sure the endpoint is not publicly accessible
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Make sure a logged in user can update the vote
        vote = Vote.objects.get(movie=self.movie1, user=self.user2)
        self.assertEqual(vote.reaction, Vote.SupportedMovieVotes.LIKE)
        token = RefreshToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token.access_token))
        data = {
            "reaction": Vote.SupportedMovieVotes.HATE
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vote.refresh_from_db()
        self.assertEqual(vote.reaction, Vote.SupportedMovieVotes.HATE)

        # Make sure a logged in user can not update a non existing vote
        url = reverse('movie_vote_list_create_update_delete', kwargs={'movie_id': self.movie4.id})
        data = {
            "reaction": Vote.SupportedMovieVotes.HATE
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_movie_vote_delete(self):
        """
        Test DELETE: /api/movies/<id>/votes
        """

        url = reverse('movie_vote_list_create_update_delete', kwargs={'movie_id': self.movie1.id})

        # Make sure the endpoint is not publicly accessible
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Make sure a logged in user can delete the vote
        token = RefreshToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token.access_token))
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Make sure a logged in user can not delete a non existing vote
        url = reverse('movie_vote_list_create_update_delete', kwargs={'movie_id': self.movie4.id})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
