from django import template
from django.conf import settings

from Core.models import CompanyData

register = template.Library()


@register.simple_tag()
def get_GOOGLE_RECAPTCHA_SITE_KEY():
    return settings.GOOGLE_RECAPTCHA_SITE_KEY


@register.simple_tag()
def get_company_data(company_data_param: str):
    try:
        return CompanyData.objects.get(name=company_data_param).value
    except CompanyData.DoesNotExist:
        return f'"{company_data_param}" not found in CompanyData.'
