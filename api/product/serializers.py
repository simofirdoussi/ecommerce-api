"""
Product serializers.
"""

from core.models import (
    Product,
    Review)

from rest_framework import serializers


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
