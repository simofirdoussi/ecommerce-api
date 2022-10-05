"""
Order APIs unit tests.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Order
from product.serializers import (
    OrderSerializer,
    OrderDetailSerializer)


ORDERS_URL = reverse('product:order-list')
ORDERS_PRIVATE_URL = reverse('product:orderprivate-list')


def order_detail_url(order_id):
    return reverse('product:order-detail', args=[order_id])


def create_user(email='email@mail.com', password='password1234'):
    """Creates and returns a user"""
    return get_user_model().objects.create(
        email=email,
        password=password,
    )


def create_admin_user(email='email@admin.com', password='password1234'):
    """Creates and returns a user"""
    return get_user_model().objects.create_superuser(
        email=email,
        password=password,
    )


def create_order(user, **params):
    """Creates and returns an order"""
    defaults = {
        'price': Decimal('7.99'),
        'done': False,
        'processed_at': timezone.now(),
    }
    defaults.update(params)
    return Order.objects.create(user=user, **defaults)


class PublicOrderTest(TestCase):
    """Public test cases for Order endpoints."""

    def setUp(self):
        self.client = APIClient()

    def test_user_not_auth(self):
        """Testing user not authenticated."""
        res = self.client.get(ORDERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrderTests(TestCase):
    """Order test cases"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()

        self.client.force_authenticate(self.user)

    def test_retrieve_orders_user(self):
        """Test retrieve orders specific to user."""
        create_order(user=self.user)
        create_order(user=self.user, price=Decimal('6.99'))
        other_user = create_user(
            email='other@mail.com',
        )
        create_order(user=other_user)
        res = self.client.get(ORDERS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        orders = Order.objects.filter(user=self.user)
        self.assertEqual(orders.count(), 2)

        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_create_order(self):
        """Testing the creation of an order."""
        payload = {
            'user': self.user.id,
            'price': Decimal('7.99'),
            'done': False,
            'processed_at': timezone.now(),
        }
        res = self.client.post(ORDERS_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        orders = Order.objects.filter(pk=res.data['id'])
        self.assertEqual(orders.count(), 1)
        order = orders[0]
        serializer = OrderDetailSerializer(order)
        self.assertEqual(res.data, serializer.data)

    def test_create_order_for_other_user_error(self):
        """Testing the creation of an order for another user returns error"""
        other_user = create_user(
            email='other@mail.com'
        )
        payload = {
            'user': other_user.id,
            'price': Decimal('7.99'),
            'done': False,
            'processed_at': timezone.now(),
        }
        res = self.client.post(ORDERS_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        orders = Order.objects.filter(pk=res.data['id'])
        self.assertEqual(orders.count(), 1)
        order = orders[0]

        self.assertEqual(order.user, self.user)

    def test_update_order_user_error(self):
        """Test updating an order returns error."""
        order = create_order(user=self.user)
        payload = {
            'price': Decimal('8.99'),
            'done': True,
            'processed_at': timezone.now(),
        }
        url = order_detail_url(order.id)
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        orders = Order.objects.filter(pk=order.id)
        self.assertEqual(orders.count(), 1)
        order = orders[0]

        self.assertNotEqual(order.price, payload['price'])
        self.assertFalse(order.done)
        self.assertNotEqual(str(order.processed_at),
                            str(payload['processed_at']))


class PrivateAdminOrderTests(TestCase):
    """Private admin order test cases."""

    def setUp(self):
        self.client = APIClient()
        self.admin_user = create_admin_user()

        self.client.force_authenticate(self.admin_user)

    def test_retrieve_all_orders(self):
        """Test the retrieval of all orders."""
        user1 = create_user()
        user2 = create_user(
            email='email2@gmail.com'
        )
        create_order(user=user1)
        create_order(user=user2)

        res = self.client.get(ORDERS_PRIVATE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)

        self.assertEqual(res.data, serializer.data)
