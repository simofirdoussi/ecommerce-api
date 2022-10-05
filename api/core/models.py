"""
Project models.
"""
import os
import uuid

from django.db import models
from django.contrib.auth.base_user import (
    BaseUserManager,
    AbstractBaseUser,
    )
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings


def product_image_file_path(instance, filename):
    """Generate file path for new product image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'product', filename)


class UserManager(BaseUserManager):
    """Base user manager."""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a User with the given email and password"""

        if not email:
            raise ValueError('Users must have an email address.')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates a superuser with is_staff and is_superuser to true."""

        user = self.create_user(
            email=email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        max_length=255,
        null=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Product(models.Model):
    """Product entity class."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    title = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, upload_to=product_image_file_path)

    def __str__(self):
        return self.title


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    done = models.BooleanField(default=False)
    processed_at = models.DateTimeField(auto_now_add=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
