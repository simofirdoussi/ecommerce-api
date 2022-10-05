"""
OrderItem APIs tests.
"""
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from core.models import(
    Order,
    Product,
    OrderItem)
from product.serializers import OrderItemSerializer


ORDERITEMS_URL = reverse('product:orderitem-list')


def create_user(email='email@mail.com', password='password1234'):
    """Creates and returns a user"""
    return get_user_model().objects.create_user(
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


def create_product(user, **params):
    """Creates and returns a product."""
    defaults = {
        'title': 'Product title',
        'description': 'descripition of the product',
        'price': Decimal('5.50'),
    }
    defaults.update(params)

    return Product.objects.create(user=user, **defaults)


def create_orderItem(order, product, **params):
    """Creates and returns orderitem."""
    defaults = {
        'name': 'orderitem default name.',
        'price': Decimal('5.50'),
    }
    defaults.update(params)

    return OrderItem.objects.create(
        order=order,
        product=product,
        **defaults
    )


def orderitem_detail_url(orderitem_id):
    """Returns an orderitem detail url."""
    return reverse('product:orderitem-detail', args=[orderitem_id])


class PublicOrderItemAPITest(TestCase):
    """Public test cases for OrderItem endpoints."""

    def setUp(self):
        self.client = APIClient()

    def test_user_not_auth(self):
        """Testing user not authenticated."""
        res = self.client.get(ORDERITEMS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrderItemAPITest(TestCase):
    """Private test cases for OrderItem"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()

        self.client.force_authenticate(self.user)

    def test_retrieve_orderitems_user(self):
        """Test retrieving orderitem specific to user."""
        product1 = create_product(user=self.user)
        product2 = create_product(user=self.user, title='product title 2')
        order = create_order(user=self.user)
        create_orderItem(order=order, product=product1)
        create_orderItem(order=order, product=product2)
        other_user = create_user(
            email='other@mail.com'
        )
        other_order = create_order(user=other_user)
        create_orderItem(order=other_order, product=product1)

        res = self.client.get(ORDERITEMS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        orderItems = OrderItem.objects.filter(order__user=self.user)
        self.assertEqual(orderItems.count(), 2)
        serializer = OrderItemSerializer(orderItems, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_retrieve_orderitem_user(self):
        """Test retrieving one orderitem for user."""
        product = create_product(user=self.user)
        order = create_order(user=self.user )
        orderItem = create_orderItem(order=order, product=product)
        url = orderitem_detail_url(orderItem.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        orderItems = OrderItem.objects.filter(pk=res.data['id'])
        self.assertEqual(orderItems.count(), 1)
        orderItem = orderItems[0]
        serializer = OrderItemSerializer(orderItem)

        self.assertEqual(res.data, serializer.data)

    def test_create_orderitem_user(self):
        """Testing the creation of a users orderitem."""
        product = create_product(user=self.user)
        order = create_order(user=self.user)

        payload = {
            'product': product.id,
            'order': order.id,
            'name': 'orderitem default name.',
            'price': Decimal('5.50'),
        }
        res = self.client.post(ORDERITEMS_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        orderitems = OrderItem.objects.filter(order=order)
        self.assertEqual(orderitems.count(), 1)
        orderitem = orderitems[0]

        serializer = OrderItemSerializer(orderitem)

        self.assertEqual(res.data, serializer.data)

    def test_update_orderitem_error(self):
        """Test update orderitem user error."""
        product = create_product(user=self.user)
        order = create_order(user=self.user)

        orderitem = create_orderItem(order=order, product=product)
        payload = {
            'name': 'orderitem updated name.',
            'price': Decimal('6.50'),
        }
        url = orderitem_detail_url(orderitem.id)
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        orderitem.refresh_from_db()

        self.assertNotEqual(orderitem.name, payload['name'])
        self.assertNotEqual(orderitem.price, payload['price'])
