"""
Testing the user APIs.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


LOGIN_URL = reverse('user:login')
CREATE_USER_URL = reverse('user:register')
MANAGE_USER_URL = reverse('user:manage-user')


def user_detail_url(user_id):
    """Returns the detail url"""
    return reverse('user:manage-user', args=[user_id])


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Testing public user APIs."""

    def setUp(self):
        self.client = APIClient()

    def test_user_login_successful(self):
        """Testing the user login returns access and refresh."""

        user_details = {
            'name': 'Name test',
            'email': 'email@gmail.com',
            'password': 'test-pw-user-123',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(LOGIN_URL, payload, format='json')

        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
        self.assertIn('email', res.data)
        self.assertIn('name', res.data)
        self.assertIn('superuser', res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_success(self):
        """Test creating user is successful."""

        user_details = {
            'name': 'Name test',
            'email': 'email@gmail.com',
            'password': 'test-pass123',
        }
        res = self.client.post(CREATE_USER_URL, user_details, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user_details['email'], res.data['email'])
        self.assertEqual(user_details['name'], res.data['name'])


class PrivateUserApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            name='Name test',
            email='email@gmail.com',
            password='test-pass123',
        )
        self.client.force_authenticate(self.user)

    """Testing the private api tests."""
    def test_full_user_update(self):
        """Test updating user."""
        user = self.user
        payload = {
            'name': 'Name update',
            'email': 'emailupdated@gmail.com',
            'password': 'test-pass1234',
        }
        res = self.client.put(MANAGE_USER_URL, payload, format='json')

        user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(user.name, payload['name'])
        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_partial_user_update(self):
        """Test partially updating user."""
        user = self.user
        payload = {
            'name': 'Name update',
            'password': 'test-pass1234',
        }
        res = self.client.patch(MANAGE_USER_URL, payload, format='json')

        user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(user.name, payload['name'])
        self.assertTrue(user.check_password(payload['password']))
