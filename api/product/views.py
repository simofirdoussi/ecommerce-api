"""
Product APIs.
"""

from .serializers import (
    ProductDetailSerializer,
    ProductSerializer,
    )
from core.models import Product

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Product api readonly viewset."""
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        else:
            return self.serializer_class


class ProductPrivateViewSet(viewsets.ModelViewSet):
    """Product api viewset."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        """Assigns the user to the product object."""
        serializer.save(user=self.request.user)
