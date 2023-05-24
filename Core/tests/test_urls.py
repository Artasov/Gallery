from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from APP_shop import views as shop_views
from APP_cart import views as cart_views
from Core import views


class UrlsTest(SimpleTestCase):
    def test_admin_url(self):
        url = reverse('admin:index')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'admin:index')

    def test_signup_url(self):
        url = reverse('signup')
        resolver = resolve(url)
        self.assertEqual(resolver.func, views.signup)

    def test_signup_confirmation_url(self):
        url = reverse('signup_confirmation', args=['confirmation_code'])
        resolver = resolve(url)
        self.assertEqual(resolver.func, views.signup_confirmation)
        self.assertEqual(resolver.kwargs['confirmation_code'], 'confirmation_code')

    def test_signin_url(self):
        url = reverse('signin')
        resolver = resolve(url)
        self.assertEqual(resolver.func, views.signin)

    def test_logout_url(self):
        url = reverse('logout')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, auth_views.LogoutView)

    def test_password_reset_url(self):
        url = reverse('password_reset')
        resolver = resolve(url)
        self.assertEqual(resolver.func, views.password_reset)

    def test_password_reset_confirmation_url(self):
        url = reverse('password_reset_confirmation', args=['confirmation_code'])
        resolver = resolve(url)
        self.assertEqual(resolver.func, views.password_reset_confirmation)
        self.assertEqual(resolver.kwargs['confirmation_code'], 'confirmation_code')

    def test_about_url(self):
        url = reverse('about')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, TemplateView)
        self.assertEqual(resolver.func.view_initkwargs['template_name'], 'Core/about.html')

    def test_terms_and_conditions_url(self):
        url = reverse('terms_and_conditions')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, TemplateView)
        self.assertEqual(resolver.func.view_initkwargs['template_name'], 'Core/terms_and_conditions.html')

    def test_privacy_policy_url(self):
        url = reverse('privacy_policy')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, TemplateView)
        self.assertEqual(resolver.func.view_initkwargs['template_name'], 'Core/privacy_policy.html')

    def test_addresses_url(self):
        url = reverse('addresses')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, TemplateView)
        self.assertEqual(resolver.func.view_initkwargs['template_name'], 'Core/addresses.html')

    def test_contacts_url(self):
        url = reverse('contacts')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, TemplateView)
        self.assertEqual(resolver.func.view_initkwargs['template_name'], 'Core/contacts.html')

    def test_profile_url(self):
        url = reverse('profile')
        resolver = resolve(url)
        self.assertEqual(resolver.func, views.profile)

    def test_main_url(self):
        url = reverse('main')
        resolver = resolve(url)
        self.assertEqual(resolver.func, views.main)


