from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="test@user.com", password="foo"
        )
        self.assertEqual(user.email, "test@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="foo"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )


class UserRegisterTest(TestCase):
    url_name = 'user-register'

    def setUp(self):
        self.User = get_user_model()
        self.name = 'Test Test'
        self.wrong_email = 'test_email'
        self.email = 'test@user.com'
        self.short_password = 'pass'
        self.password = 'password'
        self.credentials = {
            'email': self.email,
            'name': self.name,
            'password': self.password
        }

    def _user_objects_count(self, users_number):
        users = self.User.objects.all()
        self.assertEqual(users.count(), users_number)

    def test_employee_register_200(self):
        response = self.client.post(
            reverse(self.url_name), data=self.credentials
        )
        self.assertEqual(response.status_code, 200)
        self._user_objects_count(1)

    def test_employee_register_email(self):
        self.credentials['email'] = self.wrong_email
        response = self.client.post(
            reverse(self.url_name), data=self.credentials
        )
        self.assertEqual(response.status_code, 400)
        self._user_objects_count(0)

    def test_employee_register_unique_email(self):
        self.User.objects.create_user(**self.credentials)
        response = self.client.post(
            reverse(self.url_name), data=self.credentials
        )
        self.assertEqual(response.status_code, 400)
        self._user_objects_count(1)

    def test_employee_register_name(self):
        self.credentials.pop('name')
        response = self.client.post(
            reverse(self.url_name), data=self.credentials
        )
        self.assertEqual(response.status_code, 400)
        self._user_objects_count(0)

    def test_employee_register_password(self):
        self.credentials['password'] = self.short_password
        response = self.client.post(
            reverse(self.url_name), data=self.credentials
        )
        self.assertEqual(response.status_code, 400)
        self._user_objects_count(0)


class UserLoginTest(TestCase):
    url_name = 'user-login'

    def setUp(self):
        User = get_user_model()
        password = 'password'
        user = User.objects.create_user(
            email='test@user.com', password=password
        )
        self.credentials = {'email': user.email, 'password': password}
        self.client = Client()

    def test_employee_login_200(self):
        response = self.client.post(
            reverse(self.url_name),
            data=self.credentials
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json().get('access'))

    def test_employee_login_400(self):
        self.credentials['password'] += 'test'
        response = self.client.post(
            reverse(self.url_name),
            data=self.credentials
        )
        self.assertEqual(response.status_code, 401)

