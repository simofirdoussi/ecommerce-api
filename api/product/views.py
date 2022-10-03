"""
Product APIs.
"""

from .serializers import (
    ProductSerializer,
    )
from core.models import Product

from rest_framework import viewsets


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Product api readonly viewset."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
