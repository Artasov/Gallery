from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag()
def get_GOOGLE_RECAPTCHA_SITE_KEY():
    return settings.GOOGLE_RECAPTCHA_SITE_KEY
