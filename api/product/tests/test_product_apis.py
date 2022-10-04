"""
Product APIs unit tests.
"""
from decimal import Decimal

from product.serializers import (
    ProductSerializer,
    ProductDetailSerializer
)

from core.models import Product

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


PRODUCTS_URL = reverse('product:product-list')

PRODUCTS_PRIVATE_URL = reverse('product:privateproduct-list')


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


def product_detail_url(product_id):
    """Returns the product detail url."""
    return reverse('product:product-detail', args=[product_id])


def product_detail_private_url(product_id):
    """Returns the product detail private url."""
    return reverse('product:privateproduct-detail', args=[product_id])


class PublicProductApiTest(TestCase):
    """Public product apis unit tests."""

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

    def test_retrieve_detail_product(self):
        """Test retrieving a single product."""
        user = create_user()
        product = create_product(user=user)
        url = product_detail_url(product.id)
        res = self.client.get(url)

        product = Product.objects.get(pk=product.id)
        serializer = ProductDetailSerializer(product)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class PrivateProductApiTest(TestCase):
    """Private product apis unit tests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()

        self.client.force_authenticate(self.user)

    def test_retrieve_products(self):
        """Test retrieving specific user products."""

        create_product(user=self.user)
        create_product(user=self.user, title='title product')
        other_user = create_user(
            email='other@mail.com',
            password='password1234',
        )
        create_product(user=other_user, title='title product')

        products = Product.objects.filter(user=self.user)
        serializer = ProductSerializer(products, many=True)

        res = self.client.get(PRODUCTS_PRIVATE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(products.count(), 2)

        self.assertEqual(res.data, serializer.data)

    def test_create_product(self):
        """Test the creation of a product."""
        payload = {
            'title': 'Product title',
            'description': 'descripition of the product',
            'price': Decimal('5.50'),
        }
        res = self.client.post(PRODUCTS_PRIVATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        product = Product.objects.get(pk=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(product, k), v)

        self.assertEqual(product.user, self.user)

    def test_partial_update_product(self):
        """Testing the partial update of a product."""
        payload = {
            'title': 'title product updated',
            'price': Decimal(7),
        }
        product = create_product(user=self.user)
        url = product_detail_private_url(product.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        product.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(product, k), v)

        self.assertEqual(product.user, self.user)

    def test_full_update_product(self):
        """Testing the full update of a product object."""
        payload = {
            'title': 'title product updated',
            'description': 'Description product updated.',
            'price': Decimal(7),
        }
        product = create_product(user=self.user)
        url = product_detail_private_url(product.id)
        res = self.client.put(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(product, k), v)

        self.assertEqual(product.user, self.user)

    def test_delete_product(self):
        """Testing the deletion of a specific product"""
        product = create_product(user=self.user)
        url = product_detail_private_url(product.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=product.id).exists())

    def test_change_user_product_error(self):
        """Returns error when trying to change user of a product instance."""
        other_user = create_user(
            email='other@mail.com',
            password='password1234',
        )
        product = create_product(user=self.user)
        url = product_detail_private_url(product.id)
        res = self.client.patch(url, {'user': other_user.id})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.user, self.user)

    def test_delete_product_user(self):
        """Test deleting other users product error"""
        other_user = create_user(
            email='other@mail.com',
            password='password1234',
        )
        product = create_product(user=other_user)
        url = product_detail_private_url(product.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Product.objects.filter(pk=product.id).exists())
