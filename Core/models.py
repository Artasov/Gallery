import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class User(AbstractUser):
    def __str__(self):
        return f'{self.username}, {self.email}'


class CompanyData(models.Model):
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=250)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Данные компании'
        verbose_name_plural = 'Данные компании'


class Promo(models.Model):
    title = models.CharField(max_length=250)
    desc = models.TextField()
    image = models.ImageField(upload_to='promos/')

    date_published = models.DateTimeField(default=timezone.now)
    date_expired = models.DateTimeField(null=True)

    date_created = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Заменяем русские символы в названии файла на транслит
        if self.image:
            filename = self.image.name
            new_filename = slugify(filename)
            self.image.name = os.path.join('promos/', new_filename)

        super().save(*args, **kwargs)
    class Meta:
        ordering = ('date_published',)
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'


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
