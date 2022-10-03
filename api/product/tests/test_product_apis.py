"""
Product APIs unit tests.
"""
from decimal import Decimal
from product.serializers import ProductSerializer

from core.models import Product

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


PRODUCTS_URL = reverse('product:product-list')


def create_product(user, **params):
    """Creates and returns a product."""
    defaults = {
        'title': 'Product title',
        'description': 'descripition of the product',
        'price': Decimal('5.50'),
    }
    defaults.update(params)

    return Product.objects.create(user=user, **defaults)


def create_user(email='email@mail.com', password='pass12345'):
    """Creates and returns a user."""
    return get_user_model().objects.create(
        email=email,
        password=password,
    )


class PublicProductApiTest(TestCase):
    """Public procut apis unit tests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_products(self):
        """Test retrieving a list of products."""
        user = create_user()
        create_product(user=user)
        create_product(user=user, title='title product 2')

        res = self.client.get(PRODUCTS_URL)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
