from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    image = models.ImageField(upload_to='category/img/%Y/%m/%d', blank=True, verbose_name='Картинка')
    slug = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Proba(models.Model):
    proba = models.FloatField(verbose_name='Проба')


class Product(models.Model):
    class Proba(models.TextChoices):
        gold585 = '585', _('Золото')
        gold375 = '375', _('Золото')
        silver925 = '925', _('Серебро')
        none = 'none', _('none')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=150, db_index=True, verbose_name='Наименование')
    slug = models.CharField(max_length=150, db_index=True, unique=True, verbose_name='Слаг')
    image = models.ImageField(upload_to='product/img/%Y/%m/%d', blank=True, verbose_name='Картинка')
    description = models.TextField(max_length=3000, blank=True, verbose_name='Описание')
    proba = models.CharField(max_length=20, choices=Proba.choices)
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Вес', blank=True, null=True)
    size = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Размер', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена')
    discount = models.IntegerField(blank=True, null=True, verbose_name='Скидка')
    rating = models.IntegerField(blank=True, null=True, verbose_name='Рейтинг')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')
    uploaded = models.DateTimeField(auto_now=True, verbose_name='Изменен')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('APP_shop:product_detail', args=[self.id, self.slug])
