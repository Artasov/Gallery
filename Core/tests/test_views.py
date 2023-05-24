from django.core import mail
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from Core.models import UnconfirmedUser, User


class SignupViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_signup_with_valid_data(self):
        url = reverse('signup')
        response = self.client.post(url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Core/check_email.html')

        # Check that an UnconfirmedUser is created in the database
        unconfirmed_user = UnconfirmedUser.objects.get(username='testuser')
        self.assertEqual(unconfirmed_user.email, 'test@example.com')
        self.assertTrue(unconfirmed_user.confirmation_code)

    def test_signup_with_existing_username(self):
        User.objects.create_user(username='existinguser', password='password123')
        url = reverse('signup')
        response = self.client.post(url, {
            'username': 'existinguser',
            'email': 'test@example.com',
            'password': 'password123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Core/registration/signup.html')

        # Check that no new user is created in the database
        self.assertFalse(User.objects.filter(email='test@example.com').exists())

        # Check the error message in the response context
        self.assertContains(response, 'User with this name already exists.')
