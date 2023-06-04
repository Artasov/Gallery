
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe


class User(AbstractUser):
    def __str__(self):
        return f'{self.username}, {self.email}'


class Promo(models.Model):
    title = models.CharField(max_length=250)
    desc = models.TextField()
    image = models.ImageField(upload_to='promos/')

    date_published = models.DateTimeField(default=timezone.now)
    date_expired = models.DateTimeField(null=True)

    date_created = models.DateTimeField(auto_now=True)



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
