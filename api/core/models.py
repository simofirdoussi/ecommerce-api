"""
Project models.
"""
from django.db import models
from django.contrib.auth.base_user import (
    BaseUserManager,
    AbstractBaseUser)


class UserManager(BaseUserManager):
    """Base user manager."""

    def create_user(self, email, password=None):
        """Creates and saves a User with the given email and password"""

        if not email:
            raise ValueError('Users must have an email address.')

        user = self.model(
            email=self.normalize_email(email),
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


class User(AbstractBaseUser):
    """Custom user model."""

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
