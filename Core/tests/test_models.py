from datetime import datetime

from django.test import TestCase

from Core.models import User, UnconfirmedUser, UnconfirmedPasswordReset


class UserModelTest(TestCase):
    def test_user_str_representation(self):
        # Создаем пользователя для теста
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        # Проверяем, что строковое представление соответствует ожидаемому формату
        expected_str = 'testuser, test@example.com'
        self.assertEqual(str(user), expected_str)


class UnconfirmedUserModelTest(TestCase):
    def test_unconfirmed_user_creation(self):
        # Создаем объект UnconfirmedUser
        unconfirmed_user = UnconfirmedUser.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            confirmation_code='123456',
            date_created=datetime.now()
        )

        # Проверяем, что объект был успешно создан
        self.assertIsNotNone(unconfirmed_user)
        self.assertEqual(unconfirmed_user.username, 'testuser')
        self.assertEqual(unconfirmed_user.email, 'test@example.com')
        self.assertEqual(unconfirmed_user.password, 'testpassword')
        self.assertEqual(unconfirmed_user.confirmation_code, '123456')
        self.assertIsInstance(unconfirmed_user.date_created, datetime)


class UnconfirmedPasswordResetModelTest(TestCase):
    def test_unconfirmed_password_reset_creation(self):
        # Создаем объект UnconfirmedPasswordReset
        unconfirmed_reset = UnconfirmedPasswordReset.objects.create(
            email='test@example.com',
            confirmation_code='123456',
            date_created=datetime.now()
        )

        # Проверяем, что объект был успешно создан
        self.assertIsNotNone(unconfirmed_reset)
        self.assertEqual(unconfirmed_reset.email, 'test@example.com')
        self.assertEqual(unconfirmed_reset.confirmation_code, '123456')
        self.assertIsInstance(unconfirmed_reset.date_created, datetime)