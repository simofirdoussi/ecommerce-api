"""
Tests for the review APIs.
"""
from decimal import Decimal
from core.models import (
    Review,
    Product,)

from product.serializers import (
    ReviewSerializer,
    ReviewDetailSerializer,
)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


REVIEW_URL = reverse('product:review-list')


def review_detail_url(review_id):
    """Returns the review detail url."""
    return reverse('product:review-detail', args=[review_id])


def create_user(email='email@mail.com', password='password12345'):
    """Creates and returns a user."""
    return get_user_model().objects.create(
        email=email,
        password=password
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


def create_review(product, user, **params):
    """Creates and returns a review instance."""
    defaults = {
        'name': 'review name',
        'rating': 5,
        'comment': 'this is the reviews comment',
    }
    defaults.update(params)

    return Review.objects.create(
        product=product,
        user=user,
        **defaults
    )


class PublicReviewTest(TestCase):
    """Public test cases for review endpoints."""

    def setUp(self):
        self.client = APIClient()

    def test_user_not_auth(self):
        """Testing user not authenticated."""
        res = self.client.get(REVIEW_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReviewTest(TestCase):
    """Private test cases for review endpoints."""

    def setUp(self):
        self.client = APIClient( )
        self.user = create_user()
        self.product = create_product(user=self.user)

        self.client.force_authenticate(self.user)

    def test_retrive_reviews(self):
        """Test retrieving reviews."""
        review1 = create_review(
            product=self.product,
            user=self.user
        )
        review2 = create_review(
            product=self.product,
            user=self.user
        )
        res = self.client.get(REVIEW_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_retrieve_single_review(self):
        """Test retrieving a single review."""
        review = create_review(
            product=self.product,
            user=self.user,
        )
        url = review_detail_url(review.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        review = Review.objects.get(pk=res.data['id'])
        serializer = ReviewDetailSerializer(review)

        self.assertEqual(res.data, serializer.data)

    def test_create_review(self):
        """Testing the creation of a review instance."""

        payload = {
            'user': self.user.id,
            'product': self.product.id,
            'name': 'review name',
            'rating': 5,
            'comment': 'this is the reviews comment',
        }
        res = self.client.post(REVIEW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        review = Review.objects.get(pk=res.data['id'])
        serializer = ReviewDetailSerializer(review)

        self.assertEqual(res.data, serializer.data)

    def test_update_partial_review(self):
        """Testing the partial update of each review."""
        review = create_review(
            user=self.user,
            product=self.product,
        )
        payload = {
            'name': 'review name',
            'comment': 'this is the reviews comment',
        }
        url = review_detail_url(review.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        review = Review.objects.filter(pk=res.data['id'])
        self.assertEqual(review.count(), 1)
        review = review[0]

        for k, v in payload.items():
            self.assertEqual(getattr(review, k), v)

    def test_full_update_review(self):
        """Testing the full update of a review instance."""
        review = create_review(
            user=self.user,
            product=self.product,
        )

        payload = {
            'name': 'review name',
            'rating': 5,
            'comment': 'this is the reviews comment',
        }
        url = review_detail_url(review.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        review.refresh_from_db()

        review = Review.objects.filter(pk=res.data['id'])
        self.assertEqual(review.count(), 1)
        review = review[0]

        serializer = ReviewDetailSerializer(review)
        self.assertEqual(res.data, serializer.data)


    def test_error_update_user_review(self):
        """Test updating user review returns error."""
        other_user = create_user(
            email='other@mail.com',
            password='pass1235'
        )
        review = create_review(
            user=self.user,
            product=self.product
        )
        payload = {
            'user': other_user.id
        }
        url = review_detail_url(review.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        review.refresh_from_db()

        self.assertEqual(review.user, self.user)

    def test_error_update_user_review(self):
        """Test updating review product returns error."""
        other_product = create_product(
            user=self.user,
            title='other product'
        )
        review = create_review(
            user=self.user,
            product=self.product
        )
        payload = {
            'product': other_product.id
        }
        url = review_detail_url(review.id)
        self.client.patch(url, payload, format='json')
        review.refresh_from_db()
        self.assertEqual(review.product, self.product)

    def test_delete_review(self):
        """Test the deletion of a review."""
        review = create_review(
            user=self.user,
            product=self.product
        )
        url = review_detail_url(review.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(pk=review.id).exists())

