"""
Product serializers.
"""

from core.models import Product

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer."""

    class Meta:
        model = Product
        fields = ['id', 'title', 'price']

class ProductDetailSerializer(ProductSerializer):
    """Product detail serializer."""

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['description']
