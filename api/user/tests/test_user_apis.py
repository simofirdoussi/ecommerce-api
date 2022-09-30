"""
Testing the user APIs.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


LOGIN_URL = reverse('user:login')


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
