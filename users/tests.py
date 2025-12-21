from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from .forms import UserRegisterForm


class UserModelTests(TestCase):

    def test_is_admin_role(self):
        # Arrange
        user = User.objects.create_user(
            username='admin1',
            password='12345',
            role=User.Roles.ADMIN,
            first_name='Admin',
            last_name='User'
        )

        # Act
        result = user.is_admin

        # Assert
        self.assertTrue(result)

    def test_is_master_role(self):
        user = User.objects.create_user(
            username='master1',
            password='12345',
            role=User.Roles.MASTER,
            first_name='Master',
            last_name='User'
        )
        self.assertTrue(user.is_master)

    def test_is_client_role(self):
        user = User.objects.create_user(
            username='client1',
            password='12345',
            role=User.Roles.CLIENT,
            first_name='Client',
            last_name='User'
        )
        self.assertTrue(user.is_client)

    def test_fill_name_with_first_and_last_name(self):
        user = User.objects.create_user(
            username='user1',
            password='12345',
            first_name='Иван',
            last_name='Иванов'
        )
        self.assertEqual(user.fill_name, 'Иван Иванов')

    def test_fill_name_without_names(self):
        user = User.objects.create_user(
            username='user2',
            password='12345',
            first_name='',
            last_name=''
        )
        self.assertEqual(user.fill_name, 'user2')

    def test_str_method(self):
        user = User.objects.create_user(
            username='user3',
            password='12345',
            role=User.Roles.CLIENT,
            email='test@mail.com',
            first_name='Test',
            last_name='User'
        )
        self.assertIn('client', str(user))


class UserViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_redirect_by_role_admin(self):
        user = User.objects.create_user(
            username='admin',
            password='12345',
            role=User.Roles.ADMIN,
            first_name='Admin',
            last_name='User'
        )
        self.client.login(username='admin', password='12345')

        response = self.client.get(reverse('redirect_by_role'))

        self.assertRedirects(response, reverse('admin_page'))

    def test_redirect_by_role_master(self):
        user = User.objects.create_user(
            username='master',
            password='12345',
            role=User.Roles.MASTER,
            first_name='Master',
            last_name='User'
        )
        self.client.login(username='master', password='12345')

        response = self.client.get(reverse('redirect_by_role'))

        self.assertRedirects(response, reverse('master_page'))


class UserFormTests(TestCase):

    def test_user_register_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@mail.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123'
        }

        form = UserRegisterForm(data=form_data)

        self.assertTrue(form.is_valid())
