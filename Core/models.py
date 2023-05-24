from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f'{self.username}, {self.email}'


class UnconfirmedUser(models.Model):
    username = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=250, blank=True)
    email = models.EmailField(max_length=320, blank=True)
    confirmation_code = models.CharField(max_length=50, blank=True, null=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)


class UnconfirmedPasswordReset(models.Model):
    email = models.EmailField(max_length=320, blank=True)
    confirmation_code = models.CharField(max_length=50, blank=True, null=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
