from django.db.models import Count, Q, CharField, Value, Subquery, OuterRef
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from api.models import Movie, Vote
from api.permissions import AuthenticatedCreate
from api.serializers.movie import MovieSerializer, MovieVoteSerializer


class MovieListCreate(generics.ListCreateAPIView):
    """
    get:
        Returns all user submitted movies

        Publicly accessible: Yes
        Default ordering: created date (DESC)
        Available ordering: created, title, likes, hates
        Available filters: user_id

    post:
        Submits a new movie

        Publicly accessible: No
        Required parameters: title
    """

    permission_classes = (AuthenticatedCreate,)
    serializer_class = MovieSerializer
    ordering = ('-created',)
    ordering_fields = ('created', 'title', 'likes', 'hates')
    filterset_fields = ('user_id',)

    def get_queryset(self):
        queryset = Movie.objects.select_related(
            'user'
        ).annotate(
            likes=Count('movie_votes', filter=Q(movie_votes__reaction=Vote.SupportedMovieVotes.LIKE))
        ).annotate(
            hates=Count('movie_votes', filter=Q(movie_votes__reaction=Vote.SupportedMovieVotes.HATE)),
        )

        # Add custom field to return logged in user's vote or null in case of no vote
        if self.request.user.is_anonymous:
            queryset = queryset.annotate(vote=Value(None, output_field=CharField(null=True)))
        else:
            queryset = queryset.annotate(
                vote=Subquery(
                    Vote.objects.filter(movie=OuterRef('id'), user=self.request.user).values('reaction')[:1],
                    output_field=CharField(null=True)),
            )

        return queryset.all()


class MovieVoteListCreateUpdateDelete(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    """
    get:
        Returns all votes for the requested movie

        Publicly accessible: No
        Default ordering: created date (DESC)
        Available filters: reaction

    post:
        Creates a new vote for the requested movie

        Publicly accessible: No
        Required parameters: reaction

    put:
        Updates the vote for the requested movie

        Publicly accessible: No
        Required parameters: reaction

    patch:
        Updates the vote for the requested movie

        Publicly accessible: No
        Required parameters: reaction

    delete:
        Deletes the vote for the requested movie

        Publicly accessible: No
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = MovieVoteSerializer
    ordering = ('-created',)
    ordering_fields = ('created',)
    filterset_fields = ('reaction',)

    def get_queryset(self):
        return Vote.objects.filter(movie_id=self.kwargs['movie_id'])

    def get_object(self):
        """
        Override get_object() to find the vote instance based on movie id & logged in user
        """

        obj = get_object_or_404(self.get_queryset(), user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj
