from django.contrib import admin
from django.utils.safestring import mark_safe

from Core.models import User, Promo


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_show', 'desc', 'date_published', 'date_expired']
    list_editable = ['desc', 'date_published', 'date_expired']

    def image_show(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' style='object-fit: cover;' height='100' />")
        return None
    image_show.__name__ = 'Картинка'
