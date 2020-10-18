from django.db import models

from api.models.movie import Movie
from api.models.user import User


class Vote(models.Model):
    """
    Model for the relation between a user and his votes to movies
    """

    class SupportedMovieVotes(models.TextChoices):
        LIKE = 'like', 'Like'
        HATE = 'hate', 'Hate'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_votes')
    reaction = models.CharField(max_length=4, choices=SupportedMovieVotes.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Users can have only one vote for a Movie
        unique_together = ('user', 'movie')
