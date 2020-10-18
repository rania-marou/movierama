from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractBaseUser):
    """
    Base model for User
    """

    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    username = models.CharField(max_length=150, blank=False, unique=True, validators=[UnicodeUsernameValidator()])
    email = models.EmailField(blank=False, null=False, unique=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
