from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import user, movie

urlpatterns = [
    # JWT
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # User resource
    path('users', user.UserListCreate.as_view(), name='user_list_create'),
    path('users/<int:pk>', user.UserDetail.as_view(), name='user_retrieve'),

    # Movie resource
    path('movies', movie.MovieListCreate.as_view(), name='movie_list_create'),

    # Movie Vote resource
    path('movies/<int:movie_id>/votes', movie.MovieVoteListCreateUpdateDelete.as_view(),
         name='movie_vote_list_create_update_delete'),
]
