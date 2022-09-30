"""
URL mapping for the user APIs.
"""

from django.urls import path
from .views import (
    MyTokenObtainPairView
)

app_name = 'user'

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
]
