from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagerTests(TestCase):
    def test_create_user_normalizes_email_and_hashes_password(self):
        user = get_user_model().objects.create_user(
            email="Learner@EXAMPLE.COM",
            password="test-password",
        )

        self.assertEqual(user.email, "Learner@example.com")
        self.assertTrue(user.check_password("test-password"))
        self.assertFalse(user.is_staff)

    def test_create_user_requires_email(self):
        with self.assertRaisesMessage(ValueError, "An email address is required."):
            get_user_model().objects.create_user(email="", password="test-password")

    def test_create_superuser_sets_admin_permissions(self):
        user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="test-password",
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
