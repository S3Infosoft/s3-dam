from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

import logging

logging.disable(logging.CRITICAL)

INDEX_URL = reverse("index")
LOGIN_URL = reverse("login")
REGISTER_URL = reverse("register")
PASSWORD_CHANGE = reverse("password_change")
PASSWORD_RESET = reverse("password_reset")
PROFILE_URL = reverse("profile")


def password_reset_confirm_url(uid, token):
    return reverse("password_reset_confirm", args=[uid, token])


class TestCaseWithUser(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@django.com", "django123"
        )


class LoginViewTestCase(TestCase):
    """
    Tests for the Login View
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@django.com",
            password="django123",
        )

    def test_login_page_loads_successfull(self):

        res = self.client.get(LOGIN_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/login.html")

    def test_login_page_redirects_successfully(self):

        res = self.client.post(LOGIN_URL, data={
            "username": "test@django.com",
            "password": "django123",
        })

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("index"))

    def test_redirects_already_logged_in(self):

        self.client.force_login(self.user)

        res = self.client.get(LOGIN_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("index"))


class RegisterViewTestCase(TestCase):

    def test_register_page_loads_successfully(self):

        res = self.client.get(REGISTER_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/register.html")

    def test_register_page_create_user(self):

        params = {
            "email": "new_user@django.com",
            "first_name": "Abhishek",
            "password1": "testPassword",
            "password2": "testPassword",
        }

        self.client.post(REGISTER_URL, data=params)

        user = get_user_model().objects.get(email=params["email"])

        self.assertEqual(user.first_name, params["first_name"])
        self.assertEqual(user.last_name, "")
        self.assertTrue(user.check_password(params["password1"]))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_register_page_redirects_correctly(self):

        params = {
            "email": "new_user@django.com",
            "first_name": "Abhishek",
            "password1": "testPassword",
            "password2": "testPassword",
        }

        res = self.client.post(REGISTER_URL, data=params)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("login"))

    def test_register_page_fails_on_duplicate_user(self):

        params = {
            "email": "new_user@django.com",
            "first_name": "Abhishek",
            "password1": "testPassword",
            "password2": "testPassword",
        }

        self.client.post(REGISTER_URL, data=params)

        params.update({"first_name": "Chester", "last_name": "Bennington"})
        res = self.client.post(REGISTER_URL, data=params)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/register.html")
        self.assertFormError(
            res,
            "form",
            "email",
            "User with this Email address already exists."
        )

    def test_register_page_redirects_on_logged_in_user(self):

        self.client.force_login(get_user_model().objects.create_user(
            email="abhie@python.com", password="django123",
        ))

        res = self.client.get(REGISTER_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("index"))


class IndexViewTestCase(TestCase):
    """"Test for the index page view"""

    def test_redirect_to_login_for_unauthenticated_user(self):

        res = self.client.get(INDEX_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, LOGIN_URL+"?next="+INDEX_URL)

    def test_page_access_to_authenticated_users(self):

        user = get_user_model().objects.create_user("test@django.com",
                                                    "django123")
        self.client.force_login(user)

        res = self.client.get(INDEX_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "index.html")


class PasswordChangeViewTestCaseLoggedOut(TestCase):
    """Test for password change when user is unauthenticated"""

    def test_redirect_to_login_for_unauthenticated_user(self):

        res = self.client.get(PASSWORD_CHANGE)

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, LOGIN_URL+"?next=/password/change/")


class PasswordChangeViewTestCaseLoggedIn(TestCaseWithUser):
    """Tests for the Password change view"""

    def setUp(self):
        super(PasswordChangeViewTestCaseLoggedIn, self).setUp()
        self.client.force_login(self.user)

    def test_page_load_successfully(self):

        res = self.client.get(PASSWORD_CHANGE)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_change_form.html")

    def test_page_changes_password_and_redirects_successfully(self):

        params = {
            "old_password": "django123",
            "new_password1": "awesome_django",
            "new_password2": "awesome_django",
        }
        res = self.client.post(PASSWORD_CHANGE, data=params)
        self.user.refresh_from_db()

        self.assertEquals(res.status_code, 302)
        self.assertRedirects(res, reverse("profile"))
        self.assertFalse(self.user.check_password(params["old_password"]))
        self.assertTrue(self.user.check_password(params["new_password1"]))

    def test_page_error_on_wrong_old_password(self):

        params = {
            "old_password": "ruby_on_rails",
            "new_password1": "testing_is_boring",
            "new_password2": "testing_is_boring",
        }

        res = self.client.post(PASSWORD_CHANGE, data=params)

        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_change_form.html")
        self.assertFormError(res,
                             "form",
                             "old_password",
                             "Your old password was entered incorrectly. "
                             "Please enter it again.")

    def test_page_error_on_repeat_password_doesnt_match(self):

        params = {
            "old_password": "django123",
            "new_password1": "testing_is_boring",
            "new_password2": "yes_it_is",
        }

        res = self.client.post(PASSWORD_CHANGE, data=params)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_change_form.html")
        self.assertFormError(res, "form",
                             "new_password2",
                             "The two password fields didn't match.")


class PasswordResetViewTestCase(TestCaseWithUser):
    """Tests for password reset view"""

    def test_page_loads_successfully(self):

        res = self.client.get(PASSWORD_RESET)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "registration/password_reset_form.html")

    def test_page_redirects_after_entering_email(self):

        res = self.client.post(PASSWORD_RESET, data={"email": self.user.email})

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("password_reset_done"))

    def test_page_sends_email_successfully(self):
        res = self.client.post(PASSWORD_RESET,
                               data={"email": "test@django.com"})
        from django.core import mail

        self.assertEqual(res.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user.email])

    def test_page_changes_password_and_redirects(self):

        params = {
            "new_password1": "its_six_am",
            "new_password2": "its_six_am",
        }

        res = self.client.post(PASSWORD_RESET,
                               data={"email": self.user.email})
        from django.core import mail

        self.assertEqual(res.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

        token = res.context[0]["token"]
        uid = res.context[0]["uid"]

        res = self.client.post(password_reset_confirm_url(uid, token))

        redirect_url = f"/password/new/{uid}/set-password/"

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, redirect_url)

        res = self.client.post(redirect_url, data=params)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("password_reset_complete"))
        self.assertTrue(self.user.check_password(params["new_password1"]))
        self.assertFalse(self.user.check_password("django123"))


class UserDetailPageUnAuth(TestCase):

    def test_redirect_to_login(self):
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "{}?next={}".format(reverse("login"),
                                                      reverse("profile")))


class UserProfileAuth(TestCaseWithUser):

    def setUp(self):
        super(UserProfileAuth, self).setUp()
        self.client.force_login(self.user)

    def test_page_load_successfully(self):
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/profile.html")

    def test_page_contains_user_model(self):
        res = self.client.get(PROFILE_URL)

        self.assertIsInstance(res.context["object"], get_user_model())

    def test_get_absolute_url_linked_correctly(self):
        res1 = self.client.get(self.user.get_absolute_url())
        res2 = self.client.get(PROFILE_URL)

        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, res1.status_code)
        self.assertEqual(res1.request["PATH_INFO"], res2.request["PATH_INFO"])
