from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import Movie, Vote
from api.serializers.user import UserSerializer


class MovieSerializer(serializers.ModelSerializer):
    """
    Movie Serializer for list and create
    """

    user = UserSerializer(read_only=True)
    likes = serializers.IntegerField(read_only=True)
    hates = serializers.IntegerField(read_only=True)
    vote = serializers.CharField(read_only=True, allow_null=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'created', 'user', 'likes', 'hates', 'vote')

    def create(self, validated_data):
        """
        Create movie
        """

        validated_data['user'] = self.context['request'].user
        return super(MovieSerializer, self).create(validated_data)


class MovieVoteSerializer(serializers.ModelSerializer):
    """
    Movie Vote Serializer for list, create and update
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = ('reaction', 'user', 'created')

    def validate(self, attrs):
        # Do not allow logged in user to vote for movies he/she submitted
        movie_id = int(self.context['request'].resolver_match.kwargs.get('movie_id'))
        if Movie.objects.filter(user=self.context['request'].user, id=movie_id).exists():
            raise ValidationError("You can not vote for movies you submitted.")

        # Do not allow logged in user to vote for a movie twice
        if self.context['request'].method == 'POST' and \
                Vote.objects.filter(user=self.context['request'].user, movie_id=movie_id).exists():
            raise ValidationError("You can not vote for this movie twice.")

        return attrs

    def create(self, validated_data):
        """
        Create vote for movie
        """

        validated_data['user'] = self.context['request'].user
        validated_data['movie_id'] = int(self.context['request'].resolver_match.kwargs.get('movie_id'))
        return super(MovieVoteSerializer, self).create(validated_data)
