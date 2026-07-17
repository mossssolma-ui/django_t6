from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser


class CustomUserModelTest(TestCase):
    """Тесты для модели CustomUser (без кастомного менеджера)"""

    def test_create_user(self):
        """Создание обычного пользователя"""
        user = CustomUser.objects.create(email="test@example.com", is_active=True)
        user.set_password("testpass123")
        user.save()
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(str(user), "test@example.com")

    def test_create_superuser(self):
        """Создание суперпользователя"""
        user = CustomUser.objects.create(email="admin@example.com", is_staff=True, is_superuser=True, is_active=True)
        user.set_password("adminpass123")
        user.save()
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.email, "admin@example.com")

    def test_user_username_is_none(self):
        """У пользователя нет поля username"""
        user = CustomUser.objects.create(email="test@example.com")
        user.set_password("testpass123")
        user.save()
        self.assertIsNone(user.username)


class RegisterViewTest(TestCase):
    """Тесты для регистрации"""

    def test_register_page_accessible(self):
        """Страница регистрации доступна"""
        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, 200)

    def test_register_user_success(self):
        """Успешная регистрация"""
        response = self.client.post(
            reverse("users:register"),
            {
                "email": "newuser@example.com",
                "password1": "securepassword123",
                "password2": "securepassword123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertTrue(CustomUser.objects.filter(email="newuser@example.com").exists())


class LoginTest(TestCase):
    """Тесты для входа"""

    def setUp(self):
        self.user = CustomUser.objects.create(email="test@example.com")
        self.user.set_password("testpass123")
        self.user.save()

    def test_login_page_accessible(self):
        """Страница входа доступна"""
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        """Успешный вход"""
        response = self.client.post(
            reverse("users:login"), {"username": "test@example.com", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 302)

    def test_login_fail_wrong_password(self):
        """Вход с неверным паролем"""
        response = self.client.post(
            reverse("users:login"), {"username": "test@example.com", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 200)
        # Django возвращает страницу входа с ошибкой


class ProfileTest(TestCase):
    """Тесты для профиля"""

    def setUp(self):
        self.user = CustomUser.objects.create(email="test@example.com")
        self.user.set_password("testpass123")
        self.user.save()
        self.client.login(username="test@example.com", password="testpass123")

    def test_profile_page_accessible(self):
        """Профиль доступен авторизованному пользователю"""
        response = self.client.get(reverse("users:profile_user"))
        self.assertEqual(response.status_code, 200)

    def test_profile_page_redirect_if_not_logged_in(self):
        """Профиль перенаправляет неавторизованного"""
        self.client.logout()
        response = self.client.get(reverse("users:profile_user"))
        self.assertEqual(response.status_code, 302)

    def test_profile_edit_page_accessible(self):
        """Страница редактирования профиля доступна"""
        response = self.client.get(reverse("users:profile_edit"))
        self.assertEqual(response.status_code, 200)
