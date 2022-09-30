"""
URL mapping for the user APIs.
"""

from django.urls import path
from .views import (
    MyTokenObtainPairView,
    CreateUserView,
    ManageUserView
)

app_name = 'user'

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('signup/', CreateUserView.as_view(), name='register'),
    path('me/', ManageUserView.as_view(), name='manage-user'),
]
