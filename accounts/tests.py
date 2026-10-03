from io import BytesIO
import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse


User = get_user_model()


class UserManagerTests(TestCase):
    def test_create_user_normalizes_email_and_hashes_password(self):
        user = User.objects.create_user(
            email="Learner@EXAMPLE.COM",
            password="test-password",
        )

        self.assertEqual(user.email, "Learner@example.com")
        self.assertTrue(user.check_password("test-password"))
        self.assertFalse(user.is_staff)

    def test_create_user_requires_email(self):
        with self.assertRaisesMessage(ValueError, "An email address is required."):
            User.objects.create_user(email="", password="test-password")

    def test_create_superuser_sets_admin_permissions(self):
        user = User.objects.create_superuser(
            email="admin@example.com",
            password="test-password",
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class AccountTestCase(TestCase):
    password = "Valid-test-pass-734!"

    def setUp(self):
        self.user = User.objects.create_user(
            email="learner@example.com",
            password=self.password,
            first_name="Ada",
            last_name="Lovelace",
        )


class RegistrationTests(TestCase):
    def test_registration_page_loads(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)

    def test_valid_registration_creates_user(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "email": "new@example.com",
                "first_name": "New",
                "last_name": "Learner",
                "password1": "A-secure-password-918!",
                "password2": "A-secure-password-918!",
            },
        )

        self.assertRedirects(response, reverse("accounts:login"))
        self.assertTrue(User.objects.filter(email="new@example.com").exists())

    def test_invalid_password_confirmation_does_not_create_user(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "email": "new@example.com",
                "password1": "A-secure-password-918!",
                "password2": "A-different-password-918!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email="new@example.com").exists())

    def test_duplicate_email_is_rejected_case_insensitively(self):
        User.objects.create_user(email="person@example.com", password="example-pass")

        response = self.client.post(
            reverse("accounts:register"),
            {
                "email": "PERSON@example.com",
                "password1": "A-secure-password-918!",
                "password2": "A-secure-password-918!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(email__iexact="person@example.com").count(), 1)


class AuthenticationTests(AccountTestCase):
    def test_login_with_email_and_password_redirects_to_profile(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": self.user.email, "password": self.password},
        )

        self.assertRedirects(response, reverse("accounts:profile"))

    def test_bad_password_and_unknown_user_show_generic_error(self):
        for email in (self.user.email, "missing@example.com"):
            response = self.client.post(
                reverse("accounts:login"),
                {"username": email, "password": "wrong-password"},
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Please enter a correct")

    def test_external_next_redirect_is_rejected(self):
        response = self.client.post(
            reverse("accounts:login") + "?next=https://example.invalid/",
            {
                "username": self.user.email,
                "password": self.password,
                "next": "https://example.invalid/",
            },
        )

        self.assertRedirects(response, reverse("accounts:profile"))

    def test_logout_requires_post_and_clears_session(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("accounts:logout")).status_code, 405)
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertNotIn("_auth_user_id", self.client.session)


class ProfileTests(AccountTestCase):
    def test_private_profile_redirects_anonymous_user_to_login(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('accounts:profile')}",
        )

    def test_authenticated_user_can_view_own_profile(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("accounts:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.email)
        self.assertContains(response, "Ada")

    def test_profile_edit_changes_only_the_signed_in_user(self):
        other = User.objects.create_user(
            email="other@example.com",
            password="Other-secure-pass-923!",
        )
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("accounts:profile_edit"),
            {
                "email": "ada@example.com",
                "first_name": "Augusta",
                "last_name": "Byron",
            },
        )

        self.assertRedirects(response, reverse("accounts:profile"))
        self.user.refresh_from_db()
        other.refresh_from_db()
        self.assertEqual(self.user.first_name, "Augusta")
        self.assertEqual(other.email, "other@example.com")

    def test_private_edit_page_rejects_anonymous_user(self):
        response = self.client.get(reverse("accounts:profile_edit"))
        self.assertEqual(response.status_code, 302)


class PasswordTests(AccountTestCase):
    def test_password_change_updates_password_and_preserves_session(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("accounts:password_change"),
            {
                "old_password": self.password,
                "new_password1": "New-secure-pass-731!",
                "new_password2": "New-secure-pass-731!",
            },
        )

        self.assertRedirects(response, reverse("accounts:password_change_done"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("New-secure-pass-731!"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_wrong_old_password_is_rejected(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("accounts:password_change"),
            {
                "old_password": "incorrect-password",
                "new_password1": "New-secure-pass-731!",
                "new_password2": "New-secure-pass-731!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.password))

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_sends_token_and_accepts_new_password(self):
        request_response = self.client.post(
            reverse("accounts:password_reset"),
            {"email": self.user.email},
        )
        self.assertRedirects(request_response, reverse("accounts:password_reset_done"))

        token = default_token_generator.make_token(self.user)
        confirm_url = reverse(
            "accounts:password_reset_confirm",
            kwargs={"uidb64": "MQ", "token": token},
        )
        first_response = self.client.get(confirm_url)
        self.assertEqual(first_response.status_code, 302)
        response = self.client.post(
            first_response["Location"],
            {
                "new_password1": "Reset-secure-pass-371!",
                "new_password2": "Reset-secure-pass-371!",
            },
        )

        self.assertRedirects(response, reverse("accounts:password_reset_complete"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Reset-secure-pass-371!"))

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_response_does_not_disclose_unknown_email(self):
        response = self.client.post(
            reverse("accounts:password_reset"),
            {"email": "missing@example.com"},
        )
        self.assertRedirects(response, reverse("accounts:password_reset_done"))


class ProfilePhotoTests(AccountTestCase):
    def setUp(self):
        super().setUp()
        self.temp_media = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_media.cleanup)
        self.media_override = override_settings(MEDIA_ROOT=self.temp_media.name)
        self.media_override.enable()
        self.addCleanup(self.media_override.disable)

    @staticmethod
    def image_upload(name="profile.png", image_format="PNG"):
        image_bytes = BytesIO()
        Image.new("RGB", (8, 8), color="blue").save(image_bytes, format=image_format)
        return SimpleUploadedFile(name, image_bytes.getvalue(), content_type="image/png")

    def test_valid_profile_photo_upload_uses_generated_name(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("accounts:profile_photo"),
            {"profile_photo": self.image_upload("original.png")},
        )

        self.assertRedirects(response, reverse("accounts:profile"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.profile_photo.name.endswith(".png"))
        self.assertNotIn("original", self.user.profile_photo.name)
        self.assertTrue(self.user.profile_photo.storage.exists(self.user.profile_photo.name))

    def test_invalid_image_and_oversized_upload_are_rejected(self):
        self.client.force_login(self.user)
        invalid = SimpleUploadedFile("fake.png", b"not an image", content_type="image/png")
        response = self.client.post(
            reverse("accounts:profile_photo"), {"profile_photo": invalid}
        )
        self.assertEqual(response.status_code, 200)

        oversized = SimpleUploadedFile(
            "large.png",
            b"x" * (5 * 1024 * 1024 + 1),
            content_type="image/png",
        )
        response = self.client.post(
            reverse("accounts:profile_photo"), {"profile_photo": oversized}
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.profile_photo)

    def test_replacing_photo_removes_previous_file(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("accounts:profile_photo"),
            {"profile_photo": self.image_upload("first.png")},
        )
        self.user.refresh_from_db()
        old_name = self.user.profile_photo.name

        replacement_response = self.client.post(
            reverse("accounts:profile_photo"),
            {"profile_photo": self.image_upload("second.webp", "WEBP")},
        )
        self.assertRedirects(replacement_response, reverse("accounts:profile"))

        self.user.refresh_from_db()
        self.assertNotEqual(old_name, self.user.profile_photo.name)
        self.assertFalse(
            self.user.profile_photo.storage.exists(old_name),
            f"Old file remains at {old_name} in {self.temp_media.name}",
        )


class CsrfTests(TestCase):
    def test_registration_post_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(
            reverse("accounts:register"),
            {
                "email": "csrf@example.com",
                "password1": "A-secure-password-918!",
                "password2": "A-secure-password-918!",
            },
        )
        self.assertEqual(response.status_code, 403)
