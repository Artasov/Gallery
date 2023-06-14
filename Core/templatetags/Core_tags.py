from django import template
from django.conf import settings

from Core.models import CompanyData

register = template.Library()


@register.simple_tag()
def get_GOOGLE_RECAPTCHA_SITE_KEY():
    return settings.GOOGLE_RECAPTCHA_SITE_KEY


@register.simple_tag()
def get_company_data(social_name: str):
    try:
        return CompanyData.objects.get(name=social_name).value
    except CompanyData.DoesNotExist:
        return f'"{social_name}" not found in CompanyData.'
