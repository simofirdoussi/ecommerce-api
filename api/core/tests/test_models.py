"""
Unit tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user(email='email@example.com', password='pass1234'):
    """Creates and returns a user."""
    return get_user_model().objects.create_user(
        email=email,
        password=password,
    )


def create_superuser(email='email@example.com', password='pass1234'):
    """Creates and returns a superuser."""
    return get_user_model().objects.create_superuser(
        email=email,
        password=password,
    )


class TestModels(TestCase):
    """Tests for the models."""

    def test_create_user(self):
        """Test the creation of the user."""
        email = 'user@example.com'
        password = 'password12'
        user = create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        """Testing the creation of a superuser."""
        email = 'user@example.com'
        password = 'password12'
        user = create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_normalize_email(self):
        """Testing the normalization of the entered email."""
        email_samples = [
            ['Email1@example.com', 'Email1@EXAMPLE.com'],
            ['EMAIL2@example.com', 'EMAIL2@example.com'],
            ['email3@example.com', 'email3@Example.Com'],
            ['Email4@example.com', 'Email4@EXAMPLE.COM'],
        ]

        for expected, input in email_samples:
            user = create_user(
                email=input,
            )
            self.assertEqual(user.email, expected)
