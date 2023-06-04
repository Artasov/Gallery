from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_show', 'price', 'discount', 'rating', 'available', 'created_at', 'uploaded_at']
    list_filter = ['available', 'created_at', 'uploaded_at']
    list_editable = ['price', 'discount', 'available']
    prepopulated_fields = {'slug': ('name',)}

    def image_show(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='60' />")
        return None
    image_show.__name__ = 'Картинка'
