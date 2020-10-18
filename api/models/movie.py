from django.db import models

from api.models.user import User


class Movie(models.Model):
    """
    Base model for Movie
    """

    title = models.CharField(max_length=150, blank=False, unique=True)
    description = models.TextField(blank=True, default='')
    user = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE,
                             related_name='movies_submitted')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
