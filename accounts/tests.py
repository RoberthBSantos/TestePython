from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from .models import User
from .services import create_user, create_superuser


class UserModelTest(TestCase):
    def test_create_user(self):
        user = create_user('user@example.com', 'Test', 'User', 'password')
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password('password'))

    def test_create_superuser(self):
        admin_user = create_superuser('admin@example.com', 'Admin', 'User', 'adminpassword')
        self.assertIsInstance(admin_user, User)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_email_unique(self):
        create_user('unique@example.com', 'Unique', 'User', 'password')
        with self.assertRaises(IntegrityError):
            create_user('unique@example.com', 'Another', 'User', 'password')


class UserViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }

    def test_user_creation(self):
        response = self.client.post('/users/', self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_user_creation_with_existing_email(self):
        self.client.post('/users/', self.user_data, format='json')
        response = self.client.post('/users/', self.user_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_retrieve(self):
        response = self.client.post('/users/', self.user_data, format='json')
        user_id = response.data['id']
        response = self.client.get(f'/users/{user_id}/', format='json')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data['email'], self.user_data['email'])

    def test_user_update(self):
        response = self.client.post('/users/', self.user_data, format='json')
        user_id = response.data['id']
        response = self.client.patch(f'/users/{user_id}/', {'first_name': 'Updated'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get().first_name, 'Updated')

    def test_user_delete(self):
        response = self.client.post('/users/', self.user_data, format='json')
        user_id = response.data['id']
        response = self.client.delete(f'/users/{user_id}/', format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), 0)
