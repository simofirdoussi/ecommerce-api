"""
Product serializers.
"""

from core.models import Product

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer."""

    class Meta:
        model = Product
        fields = ['title', 'price', 'description']
