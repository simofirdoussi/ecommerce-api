"""
Product APIs.
"""

from .serializers import (
    OrderDetailSerializer,
    OrderSerializer,
    ProductDetailSerializer,
    ProductSerializer,
    ReviewDetailSerializer,
    ReviewSerializer,
    OrderItemSerializer
    )
from core.models import (
    Product,
    Review,
    Order,
    OrderItem)

from rest_framework import viewsets, mixins
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


class ReviewViewSet(viewsets.ModelViewSet):
    """Product api viewset."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewSerializer
        else:
            return self.serializer_class


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """Order api viewset."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        """Sets the user to the logged in user."""
        serializer.save(user=self.request.user)


class OrderPrivateViewset(OrderViewSet,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):

    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return self.queryset


class OrderItemViewset(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """OrderItem viewset for normal users."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return self.queryset.filter(
            order__user=self.request.user
        )


