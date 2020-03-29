import os
import tempfile

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from PIL import Image

from users.models import GlobalInfo

SETTINGS_URL = reverse("api_global_settings")


class PublicAPIGlobalSettingsTestCase(APITestCase):
    """Tests for API with unauthenticated users"""

    def test_login_always_required(self):
        res = self.client.get(SETTINGS_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateAPIGlobalSettingsTestCase(APITestCase):
    """Test for API with authenticated users"""

    def setUp(self):
        self.user = get_user_model().objects.create_user("test@test.com",
                                                         "django123")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_success_with_logged_users(self):
        res = self.client.get(SETTINGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_upload_logo(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmplogo:
            img = Image.new("RGB", (10, 10))
            img.save(tmplogo, format="JPEG")
            tmplogo.seek(0)

            res = self.client.patch(SETTINGS_URL, {"logo": tmplogo},
                                    format="multipart")

            obj = GlobalInfo.objects.first()

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertIn("logo", res.data)
            self.assertTrue(os.path.exists(obj.logo.path))

            obj.logo.delete()

    def test_post_method_not_allowesd(self):
        res = self.client.post(SETTINGS_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_uploading_invalid_logo(self):
        res = self.client.patch(SETTINGS_URL, {"logo": "abba dabba jappa"},
                                format="multipart")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sending_address_more_than_limit(self):
        res = self.client.put(SETTINGS_URL, {"address": "yo"*351})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
