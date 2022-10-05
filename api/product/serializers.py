"""
Product serializers.
"""

from core.models import (
    Product,
    Review,
    Order)

from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer."""

    class Meta:
        model = Order
        fields = ['id', 'price', 'done']


class OrderDetailSerializer(OrderSerializer):
    """Detail order serializer."""

    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ['processed_at', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer."""

    class Meta:
        model = Review
        fields = ['id', 'name', 'rating']


class ReviewDetailSerializer(ReviewSerializer):
    """Review detail serializer"""

    class Meta(ReviewSerializer.Meta):
        fields = ReviewSerializer.Meta.fields + ['comment']


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer."""

    class Meta:
        model = Product
        fields = ['id', 'title', 'price']


class ProductDetailSerializer(ProductSerializer):
    """Product detail serializer."""

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['description']
