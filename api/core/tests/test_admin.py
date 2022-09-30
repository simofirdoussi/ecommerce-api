"""
Tests for the admin panel.
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


def create_superuser(email='email@super.com', password='pass1234'):
    """Creates and returns a superuser."""
    return get_user_model().objects.create_superuser(
        email=email,
        password=password,
    )


class AdminTests(TestCase):
    """Admin panel unit tests."""

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='email@email.com',
            password='password23',
            name='simow'
        )
        self.superuser = create_superuser()
        self.client.force_login(self.superuser)

    def test_user_listing(self):
        """Testing the listing of the users."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """ Test edit user page works. """
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
