"""
Product apis url mappings.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from product import views


router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register(
    'privateproducts',
    views.ProductPrivateViewSet,
    basename='privateproduct')

app_name = 'product'
urlpatterns = [
    path('', include(router.urls)),
]
