"""
Unit tests for models.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import (
    Product,
    Review)

from unittest.mock import patch

from core import models


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


def create_product(user, **params):
    """Creates and returns a product."""
    defaults = {
        'title': 'Product title',
        'description': 'descripition of the product',
        'price': Decimal('5.50'),
    }
    defaults.update(params)

    return Product.objects.create(user=user, **defaults)


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
        self.assertTrue(user.is_active)

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

    def test_create_product(self):
        """Testing the creation of a product."""
        user = create_user()
        product = Product.objects.create(
            user=user,
            title='Product title',
            description='descripition of the product',
            price=Decimal('5.50'),
        )

        self.assertEqual(str(product), product.title)

    @patch('core.models.uuid.uuid4')
    def test_file_naming_products(self, mock_uuid):
        """Testing the naming of the uploaded product image."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.product_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/product/{uuid}.jpg')

    def test_create_review(self):
        """Test the creation of a review object."""
        user = create_user()
        product = create_product(user=user)
        review = Review.objects.create(
            product=product,
            user=user,
            name='name',
            rating=4,
            comment='comment of the review',
        )

        self.assertEqual(str(review), review.name)
