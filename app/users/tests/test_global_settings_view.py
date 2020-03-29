import os
import tempfile

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from PIL import Image

from ..models import GlobalInfo

SETTINGS_URL = reverse("global_settings")


class GlobalSettingsViewUnauthenticated(TestCase):
    """Test for unauthenticated users"""

    def test_page_redirected_to_login_page(self):

        res = self.client.get(SETTINGS_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "{}?next={}".format(reverse("login"),
                                                      SETTINGS_URL))


class GlobalSettingsViewAuthenticated(TestCase):
    """Tests for authenticated users"""

    def setUp(self):
        self.user = get_user_model().objects.create_user("test@test.com",
                                                         "django123")
        self.settings_obj = GlobalInfo.objects.first()
        self.client = Client()
        self.client.force_login(self.user)

    def tearDown(self):
        self.settings_obj.logo.delete()

    def test_page_loads_successfully(self):
        res = self.client.get(SETTINGS_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/global.html")

    def test_uploading_logo_successfull(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_logo:
            image = Image.new("RGB", (10, 10))
            image.save(temp_logo, format="JPEG")
            temp_logo.seek(0)

            res = self.client.post(SETTINGS_URL,
                                   {"logo": temp_logo},
                                   format="multipart/form-data")

            self.settings_obj.refresh_from_db()

            self.assertEqual(res.status_code, 302)
            self.assertTrue(os.path.exists(self.settings_obj.logo.path))
